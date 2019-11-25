import random
#=========================================================================================
machinesList = []
"""All machines in factory"""

itinerariesList = []
"""All itineraries"""

STRGS = {
    'TITLE_PROGRAM' : "JobShop PRO",
    'ITINERARIES' : "Itineraries",
    'ADD_NEW' : "Add new",
    'ADD' : "Add",
    'EDIT' : "Edit",
    'DELETE' : "Delete",
    'DETAILS' : "Details",    
    'WARN':"Warning!",
    'ERR':"Error!",
    'ERR_ILLEGAL': "Illegal action!",
    'ERR_EXIST_DIFF_NAME':" exist. Enter diffrent name.",
    'MSG_WARN_MACH_IN_USE':" is in use by task.\nThink about whether you know what you are doing.",
    'MSG_WARN_ERASE_DATA':"Using this option will replace existing data. Are you REALLY sure?",
    'MSG_WARN_NO_EXPORT':"Nothing to export! Create machines and itineraries",
    'MSG_ERR_NO_MACH_CREATE' : "No machines were created!",
    'MSG_ERR_NO_MACH_NO_ITINERS' : "You can't create itinerary if there is no machines.",
    'MSG_ERR_ITINERARY_NO_NAME': "The itinerary have no name!",
    'MSG_ERR_ITINERARY_ENTER_NAME' : "Please, enter itinerary name.",
    'MSG_ERR_INVOLVE_TASK':"\nError involve element at: ",
    'TITLE_NEW_ITINERARIES' : "New itinerary",
    'MSG_ERR_TASK_NO_NAME':"Task have no name!",
    'MSG_ERR_TASK_ENTER_NAME' : "Please, enter task name.",
    'MSG_ERR_WRONG_VAL':"Wrong value!",
    'MSG_ERR_EMPTY_VAL':"Empty value!",
    'MSG_ERR_VALUE_NO_ZERO': "Value cannot be equal zero!",
    'MSG_ERR_TASK_CORRECT_DURATION' : "Please, check if value is correct. Duration time should be greater than zero.",
    'MSG_REALLY_QUIT':"Are you sure you want to quit program?",
    'MSG_OK_FILE_EXPORTED':"File exported sucessfully!",
    'MSG_OK_FILE_IMPORTED':"File imported sucessfully!",
    'ITINERARY_NAME' : "Itinerary name:",
    'TASK_DETAIL' : "Task detail",
    'NAME' : "Name:",
    'DURATION' : "Duration:",
    'ORDER':'Order:',
    'MACH':"Machine:",
    'MACHS': "Machines",
    'MACHS_ITINERARIES':"Machines in itineraries",
    'SAVE': 'Save',
    'MACH_DETAILS':"Machine Details",
    'ID':"ID: ",
    'OK': "OK",
    'CANCEL': "Cancel",
    'ENTER_NEW_VAL':"Enter new value: ",
    'TITLE_NEW_TASK_INITERARY':"New task in itinerary",
    'NEW_TASK':"New task",
    'TASKS_INITERARY': "Tasks in itinerary",
    'TIMES_TASKS':"Times of tasks",
    'EXIT':"Exit",
    'M_FILE_IMPORT':"Import from file...",
    'M_FILE_EXPORT':"Export to file...",
    'ABOUT':"About",
    'ABOUT_TITLE':"About JobShopPRO",
    'ABOUT_MESG':"This is JobShopPRO\nMade as Master Thesis at AGH University\nby Pawel Kastelik, 2018",
    'SETUP':'Setup',
    'DATA':"Data",
    'ENTER_MATRIX_DATA':"Enter data in matrix",
    'CALC':"Calculate",
    'CREATED':"Created ",
    'NUM_MACHS':"Number of machines:",
    'NUM_ITINERS':"Number of itineraries:"
    }
"""Dictionary with strings used to gui"""

def validateFloat(self, action, index, valueIfAllowed, maxCount, priorValue, text, validationType, triggerType, widgetName):
    """Preserve to enter only specified keys into entry not longer than maxCount digits """
    if len(valueIfAllowed) > int(maxCount): 
        return False
    elif action == '1': #Type of action (1=insert, 0=delete, -1 for others)
        if text in '0123456789.':
            try:
                float(valueIfAllowed)
                return True
            except ValueError:
                return False
        else:
            return False
    else:
        return True

def validateOnlyInt(self, action, index, valueIfAllowed, maxCount, priorValue, text, validationType, triggerType, widgetName):
    """Preserve to enter numbers specified keys into entry not longer than maxCount digits """
    if len(valueIfAllowed) > int(maxCount): 
        return False
    elif action == '1': #Type of action (1=insert, 0=delete, -1 for others)
        if text in '0123456789':
            try:
                float(valueIfAllowed)
                return True
            except ValueError:
                return False
        else:
            return False
    else:
        return True

def isStringNotBlank(stringValue):
    "if string is empty or none return false"
    return bool(stringValue and stringValue.strip())


def get_random_color(pastel_factor=0.5):
    return [(x + pastel_factor) / (1.0 + pastel_factor) for x in [random.uniform(0,1.0) for i in [1,2,3]]]

def color_distance(c1,c2):
    return sum([abs(x[0] - x[1]) for x in zip(c1,c2)])

def generate_new_color(existing_colors,pastel_factor=0.5):
    """Generate new color if not exist in existing array of colors"""
    max_distance = None
    best_color = None
    for i in range(0,100):
        color = get_random_color(pastel_factor = pastel_factor)
        if not existing_colors:
            return color
        best_distance = min([color_distance(color,c) for c in existing_colors])
        if not max_distance or best_distance > max_distance:
            max_distance = best_distance
            best_color = color
    return best_color