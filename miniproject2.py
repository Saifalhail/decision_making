list_of_assets = ['fireEngineA', 'fireEngineB', 'fireFastResponse', 'ambulance', 'medicalFastResponse', 'policePatrolCar',
                  'trafficPoliceBike']

fireEngineA = {'speed': 80, 'capability': [
    'oil', 'chemical', 'electrical'], 'prep': 5, 'effectiveness': ['supress']}
fireEngineB = {'speed': 90, 'capability': [
    'chemical', 'electrical'], 'prep_time': 3, 'effectiveness': ['supress']}
fireFastResponse = {'speed': 100, 'capability': [
    'electrical'], 'prep_time': 2, 'effectiveness': ['control']}
ambulance = {'speed': 80, 'capability': [
    'injury-serious', 'injury-light'], 'prep_time': 5, 'effectiveness': ['control', 'evacuate']}
medicalFastResponse = {'speed': 100, 'capability': [
    'injury-light'], 'prep_time': 2, 'effectiveness': ['investigate', 'arrest', 'control']}
policePatrolCar = {'speed': 100, 'capability': ['robbery', 'breakin', 'traffic accident', 'traffic control'],
                   'prep_time': 3, 'effectiveness': ['investigate', 'arrest', 'control']}
trafficPoliceBike = {'speed': 120, 'capability': [
    'traffic accident', 'traffic control'], 'prep_time': 2, 'effectiveness': ['investigate', 'control']}

situations = {'small': 1, 'medium': 2, 'large': 3, 'injury/light': 1, 'injury/serious': 1, 'crime/simple': 1, 'crime/serious': 2}

erStationA = {'fireEngineA': 5, 'fireEngineB': 2, 'fireFastResponse': 5,
              'ambulance': 2, 'medicalFastResponse': 2, 'policePatrolCar': 3, 'trafficPoliceBike': 2}

erStationB = {'fireEngineA': 2, 'fireEngineB': 1, 'fireFastResponse': 3,
              'ambulance': 2, 'medicalFastResponse': 2, 'policePatrolCar': 3, 'trafficPoliceBike': 2}

