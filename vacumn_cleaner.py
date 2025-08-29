def vacuum_world():
    # initializing goal_state
    # 0 indicates Clean and 1 indicates Dirty
    goal_state = {'A': '0', 'B': '1'}
    cost = 0
    
    # user input
    location_input = input("Enter Location of Vacuum (A or B): ")
    status_input = input("Enter status of " + location_input + " (0=Clean, 1=Dirty): ")
    status_input_complement = input("Enter status of the other room (0=Clean, 1=Dirty): ")

    print("Initial Location Condition: " + str(goal_state))

    if location_input == 'A':
        print("Vacuum is placed in Location A")

        if status_input == '1':   # A is Dirty
            print("Location A is Dirty.")
            goal_state['A'] = '0'    # clean A
            cost += 1
            print("COST for CLEANING A: " + str(cost))
            print("Location A has been Cleaned.")

            if status_input_complement == '1':  # B is Dirty
                print("Location B is Dirty.")
                print("Moving RIGHT to Location B.")
                cost += 1
                print("COST for moving RIGHT: " + str(cost))
                goal_state['B'] = '0'    # clean B
                cost += 1
                print("COST for SUCK: " + str(cost))
                print("Location B has been Cleaned.")
            else:
                print("No action. COST: " + str(cost))
                print("Location B is already clean.")

        elif status_input == '0':  # A already clean
            print("Location A is already clean.")
            if status_input_complement == '1':  # B is Dirty
                print("Location B is Dirty.")
                print("Moving RIGHT to Location B.")
                cost += 1
                print("COST for moving RIGHT: " + str(cost))
                goal_state['B'] = '0'
                cost += 1
                print("COST for SUCK: " + str(cost))
                print("Location B has been Cleaned.")
            else:
                print("No action. COST: " + str(cost))
                print("Location B is already clean.")

    else:  # Vacuum is in B
        print("Vacuum is placed in Location B")

        if status_input == '1':   # B is Dirty
            print("Location B is Dirty.")
            goal_state['B'] = '0'
            cost += 1
            print("COST for CLEANING B: " + str(cost))
            print("Location B has been Cleaned.")

            if status_input_complement == '1':  # A is Dirty
                print("Location A is Dirty.")
                print("Moving LEFT to Location A.")
                cost += 1
                print("COST for moving LEFT: " + str(cost))
                goal_state['A'] = '0'
                cost += 1
                print("COST for SUCK: " + str(cost))
                print("Location A has been Cleaned.")
            else:
                print("No action. COST: " + str(cost))
                print("Location A is already clean.")

        elif status_input == '0':  # B already clean
            print("Location B is already clean.")
            if status_input_complement == '1':  # A is Dirty
                print("Location A is Dirty.")
                print("Moving LEFT to Location A.")
                cost += 1
                print("COST for moving LEFT: " + str(cost))
                goal_state['A'] = '0'
                cost += 1
                print("COST for SUCK: " + str(cost))
                print("Location A has been Cleaned.")
            else:
                print("No action. COST: " + str(cost))
                print("Location A is already clean.")

    # Final Output
    print("GOAL STATE: ", goal_state)
    print("Performance Measurement (Total Cost): " + str(cost))
vacuum_world()
