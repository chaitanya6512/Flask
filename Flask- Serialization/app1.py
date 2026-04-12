# Serialization Method 2: Using Python's json Module

import json
data = {"name":"Charan Vegi"
        , "age":25}

# Convert JPython dict to JSON string
json_data = json.dumps(data)
print(json_data)