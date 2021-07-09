import sys
import yaml

def mergeYamlData(yamlData, newYamlData, thePath) :
  # This is a generic Python merge
  # It is a *deep* merge and handles both dictionaries and arrays
  #
  if type(yamlData) is None :
    print("ERROR yamlData should NEVER be None ")
    sys.exit(-1)

  if type(yamlData) != type(newYamlData) :
    print("Incompatible types {} and {} while trying to merge YAML data at {}".format(type(yamlData), type(newYamlData), thePath))
    print("Stoping merge at {}".format(thePath))
    return

  if type(yamlData) is dict :
    for key, value in newYamlData.items() :
      if key not in yamlData :
        yamlData[key] = value
      elif type(yamlData[key]) is dict :
        mergeYamlData(yamlData[key], value, thePath+'.'+key)
      elif type(yamlData[key]) is list :
        for aValue in value :
          yamlData[key].append(aValue)
      else :
        yamlData[key] = value
  elif type(yamlData) is list :
    for value in newYamlData :
      yamlData.append(value)
  else :
    print("ERROR yamlData MUST be either a dictionary or an array.")
    sys.exit(-1)

def loadConfig(configFile, verbose) :
  config = {
    'natsServer' : {
      'cert' : None,
      'key'  : None,
      'port' : '4222',
      'host' : 'localhost',
      },
    'watches' : []
  }
  try :
    yamlFile = open(configFile)
    yamlConfig = yaml.safe_load(yamlFile.read())
    yamlFile.close()
    mergeYamlData(config, yamlConfig, "")
  except Exception as ex :
    print("Could not load the configuration file: [{}]".format(configFile))
    print(ex)

  for aWatch in config['watches'] :
    if 'channel' not in aWatch :
      print("The watch:")
      print(aWatch)
      print("MUST specify a channel")
      sys.exit(-1)
    if 'files' not in aWatch or not isinstance(aWatch['files'], list) :
      print("The watch:")
      print(aWatch)
      print("MUST specify a list of files")
      sys.exit(-1)
    if 'ignoreFiles' in aWatch :
      if not isinstance(aWatch['ignoreFiles'], list) :
        print("The ignoreFiles in the watch:")
        print(aWatch)
        print("MUST be a list of files")
        sys.exit(-1)
    else :
      aWatch['ignoreFiles'] = []
    if 'masks' in aWatch :
      if not isinstance(aWatch['masks'], list) :
        print("The masks in the watch:")
        print(aWatch)
        print("MUST be a list of inotify mask names")
        sys.exit(-1)
    else :
      aWatch['masks'] = [ 'CREATE', 'MODIFY', 'MOVE' ]

  config['verbose'] = verbose
  if 0 < config['verbose'] :
    print("---------------------------------------------------------------")
    print("Configuration:")
    print(yaml.dump(config))
    print("---------------------------------------------------------------")

  return config
