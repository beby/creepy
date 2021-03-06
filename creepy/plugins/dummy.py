from InputPlugin import InputPlugin


class Dummy(InputPlugin):
    name = "dummy"
    configured = False
    
    
    def __init__(self):
        pass
    def activate(self):
        pass
        
    def deactivate(self):
        pass
        
    def searchForTargets(self):
        return {'pluginName':'Dummy Plugin', 'targetUsername':'dummyusername', 'targetFullname': 'dummy fullname', 'targetPicture': '303ec0c.jpg', 'targetDetails': 'Profile description'}
    
    def loadConfiguration(self):
        pass
    
    def isFunctional(self):
        return True
    
    def returnLocations(self, target, search_params):
        locations = [{'lon':38.343242,'lat':23.3213,'context':'this is the context', 'shortName':'This is the short name'},{'lon':40.343242,'lat':29.3213,'context':'this is the context2', 'shortName':'This is the short name2'}]
        return locations
    
    def returnPersonalInformation(self, search_params):
        pass
        
