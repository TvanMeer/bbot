"""

Main

"""

class Bot():

    def __init__(options):
        
        mode         = options.mode
        base_assets  = options.base_assets
        quote_assets = options.quote_assets
        windows      = options.windows

        # Get through API
        all_pairs    = {}
        pairs        = {}

        #TODO: shield all attrs with getters and setters
