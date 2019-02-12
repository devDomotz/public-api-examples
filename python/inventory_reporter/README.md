# Domotz Inventory Reporter 

A demo app for showing a mildly useful yet simple Domotz™ Public API Usage.
 
## What it does

 
`domotz_inventory_reporter` calls the Domotz Public API and creates a document containing all the devices in the 
networks managed by your Domotz Agents.

Before starting be sure to have a valid Domotz API key and its corresponding endpoint URL 
([can be obtained here](https://portal.domotz.com/portal/account)).

For having a (not empty) report, at least one agent granting API calls must be active 
([check here for plans and pricing](https://www.domotz.com/pricing.php))

## Requirements

`domotz_inventory_reporter` is written in Python 3, using the `async` ans `await` keywords. It requires Python >= 3.5.

Most Linux distributions come with Python 3.5 or newer shipped.

Windows and Mac, or older linuxes users, should find out how to install Python 3 on their computers by their own means
😀.

Some resources:

- [Installing on Mac](https://wsvincent.com/install-python3-mac/)
- [Installing on Windows](https://docs.python-guide.org/starting/install3/win/)

`git` is required for cloning and getting updates, but you can just download an archive of the project and extract it 
wherever in your disk.
 
# Installation 

## Note
These instructions were tested on OSX 10.14.2 with Python3.  


Clone the repository locally to your computer, let's call the destination directory 
(e.g `/home/iacopo/domotz_inventory_reporter`)
 `$baseDir` for short.

```bash
git clone [repository url]/domotz_inventory_reporter $baseDir
cd $baseDir
python3 -m venv env
. env/bin/activate
pip install -r requirements.txt
```


# Run

First, verify the installation was successful:
```bash
cd $baseDir
. env/bin/activate; bin/domotz_inventory_report --help
```

Then, for obtaining a report, you have to run:
```bash
bin/domotz_inventory_report -u [Your API endpoint] -k [your API key] -o report.xslx
```

## json output

Calling the program with the `-f json` flag, you will get a json containing all the data extracted from the API.

# Licence

MIT - See [LICENCE.md](./LICENCE.md)