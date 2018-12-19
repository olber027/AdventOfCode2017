#!/usr/bin/env python
# Copyright 2018, 2018 Cray Inc. All Rights Reserved.
import requests
import json
import time
import argparse
import math
import urllib3
from kafka import KafkaConsumer

# remove the insecure request warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_components(hsmComponentsUrl):
    '''
    This function returns a dictionary of components from the Hardware State Manager (HSM)
        Args:
         hsmComponentsUrl (str): The URL for the hardware state manager Components

        Returns:
         components_dictionary (dictionary): A dictionary of components from the HSM
    '''
    components = requests.get(hsmComponentsUrl, verify=False)
    components.raise_for_status()
    components_dictionary = components.json()
    return components_dictionary

def node_power_action(state, components, capmcBaseUrl, nodesToExclude=None):
    '''
    This function changes the state of the given components to the given state
        Args:
         state        (str): the state to change the components to. should be either 'On' or 'Off'.
         components  (dict): a dictionary containing the information for the components to change the state of.
         capmcBaseUrl (str): url to send the power state change command to.

        Returns:
         N/A
    '''
    targetNodes = [component['NID'] for component in components['Components'] if not nodesToExclude or component['NID'] not in nodesToExclude]

    if 'On' in state:
        print('Setting node power to On for the following nodes {}'.format(targetNodes))
        nodesToTurnOn = {'nids': targetNodes}
        capmcNodeOnCall = requests.post(capmcBaseUrl + 'node_on', json=nodesToTurnOn, verify=False)
        capmcNodeOnCall.raise_for_status()

    if 'Off' in state:
        print('Setting node power to Off for the following nodes {}'.format(targetNodes))
        nodesToTurnOff = {'nids': targetNodes}
        capmcNodeOffCall = requests.post(capmcBaseUrl + 'node_off', json=nodesToTurnOff, verify=False)
        capmcNodeOffCall.raise_for_status()

def check_power_status(components, nodesToExclude=None):
    '''
    This is a convenience function to parse through the components dictionary and return lists of nodes that are on and off
        Args:
         components (dict): dictionary containing all the component information

        Returns:
         nodeTuple (tuple): a tuple with the first value being a list of nodes that are on, and the second being
                            the list of the nodes that are off.
    '''
    nodesThatAreOn = []
    nodesThatAreOff = []
    for component in components['Components']:
        if nodesToExclude and component['NID'] in nodesToExclude:
            continue
        if component['State'] in ('Ready'):
            nodesThatAreOn.append(component)
        elif component['State'] in ('On', 'Standby', 'Off'):
            nodesThatAreOff.append(component)

    return nodesThatAreOn, nodesThatAreOff

def get_kafka_messages_after_time(kafkaAddress, cutoffTimeStamp):
    '''
    This function searches for and returns any messages from kafka that were sent after the given time
        Args:
         kafkaAddress    (str): the address to make the query to kafka from
         cutoffTimeStamp (int): the earliest time that we would want to retrieve messages from

        Returns:
         messages       (dict): a dictionary with xnames as the keys and the time of the first
                                heartbeat for that xname as the value.
    '''
    messages = {}

    # Creating the kafka consumer
    consumer = KafkaConsumer('heartbeat_notifications',
                             bootstrap_servers=[kafkaAddress],
                             consumer_timeout_ms=10000,
                             auto_offset_reset='earliest')
    # Reading messages from the consumer
    heartbeatStarted = 'Heartbeat started.'
    for message in consumer:
        hbtd_message = json.loads(message.value)
        if message.timestamp > cutoffTimeStamp and heartbeatStarted in hbtd_message['Info']:
            if hbtd_message['ID'] not in messages:
                messages[hbtd_message['ID']] = message.timestamp
    return messages

def to_minutes_and_seconds(microseconds):
    '''
    This function converts a given value in microseconds to a corresponding number of minutes and seconds
        Args:
         microseconds (number): value to convert, given in microseconds

        Returns:
         time          (tuple): a tuple containing the time in minutes and seconds, both as integers
    '''
    seconds = microseconds / 1000.0
    minutes = int(seconds / 60)
    seconds -= (minutes * 60)

    return (minutes, int(seconds))

def get_boot_message(unformattedMessage, bootNumber):
    '''
    This is a convenience function to print the boot message prettily
        Args:
         unformattedMessage (str): message to print. should include a formatting spot for the boot number
         bootNumber         (int): the number of the boot to print

        Returns:
         message            (str): the nicely formatted message
    '''
    message = unformattedMessage.format(bootNumber)
    if len(message) % 2 == 1:
        message += " "
    numDashes = (80 - len(message)) / 2
    return ("-" * numDashes) + message + ("-" * numDashes)

def print_summary(components, numSequences, bootFailures, shutdownFailures, excludedNIDs):
    '''
    This function prints a summary of the results we collected
        Args:
         components       (dict): a dictionary containing the component information,
                                  including a list of boot times
         numSequences      (int): number of boot sequences that were ran
         bootFailures      (set): set of NIDs that experienced boot failures
         shutdownFailures  (set): set of NIDs that experienced a shutdown failure
         excludedNIDs     (list): list of NIDs excluded from the run

        Returns:
         N/A
    '''
    numBoots = 0.0
    totalBootTime = 0
    componentsBooted = 0
    fastest = 10000000000
    standardDeviation = 0.0
    fastestNID = 0
    slowest = 0
    slowestNID = 0

    print(get_boot_message("average boot time by NID{}", ""))

    for component in sorted(components["Components"], key=(lambda x: x['NID'])):
        if "boot_times" not in component:
            continue

        componentsBooted += 1
        numComponentBoots = 0
        componentBootTime = 0

        for time in component["boot_times"]:
            numComponentBoots += 1
            componentBootTime += time
            standardDeviation += time*time
            if time < fastest:
                fastest = time
                fastestNID = component['NID']
            if time > slowest:
                slowest = time
                slowestNID = component['NID']

        NIDBootTime = to_minutes_and_seconds(componentBootTime/numComponentBoots)
        print("NID {} : {} minutes {} seconds".format(component['NID'], NIDBootTime[0], NIDBootTime[1]))

        totalBootTime += componentBootTime
        numBoots += numComponentBoots

    if numBoots == 0:
        print("all nodes failed to boot...")
        exit(1)

    average = totalBootTime/numBoots
    standardDeviation = math.sqrt((standardDeviation/numBoots) - (average * average))

    average           = to_minutes_and_seconds(average)
    standardDeviation = to_minutes_and_seconds(standardDeviation)
    fastestTime       = to_minutes_and_seconds(fastest)
    slowestTime       = to_minutes_and_seconds(slowest)

    print("\nboot sequences run        : {}".format(numSequences))
    print("total boot times recorded : {}".format(componentsBooted))
    print("total boot failures       : {}".format(len(bootFailures)))
    print("total shutdown failures   : {}".format(len(shutdownFailures)))
    print(get_boot_message("boot time summary{}", ""))
    print("average node boot time    : {} minutes {} seconds".format(average[0], average[1]))
    print("standard deviation        : {} minutes {} seconds".format(standardDeviation[0], standardDeviation[1]))
    print("fastest boot time         : {} minutes {} seconds (NID {})".format(fastestTime[0], fastestTime[1], fastestNID))
    print("slowest boot time         : {} minutes {} seconds (NID {})".format(slowestTime[0], slowestTime[1], slowestNID))
    if bootFailures:
        print("\nnodes that failed to boot    : {}".format(sorted([fail for fail in bootFailures])))
    if shutdownFailures:
        print("\nnodes that failed to shutdown: {}".format(sorted([fail for fail in shutdownFailures])))
    if excludedNIDs:
        print("\nnodes excluded from this run : {}".format(sorted(excludedNIDs)))

def main():

    parser = argparse.ArgumentParser(description="Tool to get average boot times for nodes")
    parser.add_argument('-s', '--hsm_components_url', required=True, action='store',
                        help="url pointing to the components endpoint")
    parser.add_argument('-c', '--capmc_url', required=True, action='store',
                        help="url pointing to the capmc endpoint")
    parser.add_argument('-t', '--timeout', required=False, action='store', default=600,
                        help="max time to wait for all the nodes to be powered on or off")
    parser.add_argument('-r', '--retry_time', required=False, action='store', default=60,
                        help="time to wait between checking if the nodes are on or off")
    parser.add_argument('-n', '--num_boot_sequences', required=False, action='store', default=1,
                        help="number of times to run the boot sequence")
    parser.add_argument('-k', '--kafka_address', required=True, action='store',
                        help="The address of the kafka topic")
    parser.add_argument('-e', '--exclude', required=False, action='store',
                        help="comma separated list of NIDs to exclude")

    arguments = parser.parse_args()

    componentsURL = arguments.hsm_components_url
    components    = get_components(componentsURL)
    capmcURL         = arguments.capmc_url
    numBootSequences = int(arguments.num_boot_sequences)
    maxTimeout       = int(arguments.timeout)
    retryTime        = int(arguments.retry_time)
    excluded         = arguments.exclude
    kafkaAddress     = arguments.kafka_address

    nodesThatFailedToBoot = set()
    nodesThatFailedToShutdown = set()

    for _ in range(numBootSequences):
        print(get_boot_message("start of boot {}", _))

        nodesToExclude = [int(NID.strip()) for NID in excluded.split(",")] if excluded else []
        node_power_action("Off", components, capmcURL, nodesToExclude)

        elapsedTime = 0
        nodesPoweredOn = True
        nodeStatuses = check_power_status(components, nodesToExclude)
        while nodesPoweredOn and elapsedTime < maxTimeout:
            print("{} nodes are still on. waiting on NIDs:\n{}".format(len(nodeStatuses[0]), [node['NID'] for node in nodeStatuses[0]]))
            print("Waiting another {} seconds... ({} of {} seconds waited so far)".format(retryTime, elapsedTime, maxTimeout))
            time.sleep(retryTime)
            elapsedTime += retryTime
            components = get_components(componentsURL)
            nodeStatuses = check_power_status(components, nodesToExclude)
            nodesPoweredOn = len(nodeStatuses[0]) > 0

        if nodesPoweredOn:
            print("Some of the nodes were not powered off in the given time frame.")
            print("The following nodes were still on and will be excluded from the metrics.")
            nidList = [node['NID'] for node in nodeStatuses[0]]
            print(nidList)
            [nodesToExclude.append(nid) for nid in nidList]
            [nodesThatFailedToShutdown.add(nid) for nid in nidList]
        else:
            print("\nall the nodes were shut down successfully")

        print("-" * 80)

        bootStartTime = int(time.time() * 1000)
        node_power_action("On", components, capmcURL, nodesToExclude)

        nodesPoweredOff = True
        nodeStatuses = check_power_status(components, nodesToExclude)
        elapsedTime = 0
        while nodesPoweredOff and elapsedTime < maxTimeout:
            print("{} nodes are still off. waiting on NIDs:\n{}".format(len(nodeStatuses[1]), [node['NID'] for node in nodeStatuses[1]]))
            print("Waiting another {} seconds... ({} of {} seconds waited so far)".format(retryTime, elapsedTime, maxTimeout))
            time.sleep(retryTime)
            elapsedTime += retryTime
            components = get_components(componentsURL)
            nodeStatuses = check_power_status(components, nodesToExclude)
            nodesPoweredOff = len(nodeStatuses[1]) > 0

        nodesStillOff = [node['NID'] for node in nodeStatuses[1]]
        if nodesPoweredOff:
            print("Some of the nodes were not powered back on in the given time frame.")
            print("The following nodes were still down and will be excluded from the metrics")
            print(nodesStillOff)
            [nodesToExclude.append(node) for node in nodesStillOff]
            [nodesThatFailedToBoot.add(node) for node in nodesStillOff]
        else:
            print("all the nodes were powered back on successfully")

        messages = get_kafka_messages_after_time(kafkaAddress, bootStartTime)

        for component in components['Components']:
            # ignore any nodes that failed to boot
            if component['NID'] in nodesToExclude:
                continue

            if "boot_times" not in component:
                component["boot_times"] = []
            component["boot_times"].append(messages[component['ID']] - bootStartTime)
        print(get_boot_message("end of boot {}", _))

    excludedNIDList = [int(NID.strip()) for NID in excluded.split(",")] if excluded is not None else []
    print_summary(components, numBootSequences, nodesThatFailedToBoot, nodesThatFailedToShutdown, excludedNIDList)

if __name__ == "__main__":
    main()
