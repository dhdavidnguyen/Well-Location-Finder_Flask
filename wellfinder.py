import pandas as pd
import logging
from flask import Flask, request, abort, render_template
from urllib.parse import urljoin

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

"""Has issue with multiple instances of well name. Need to throw exception and add additional search criteria"""



# well = '41-31R'

def wellnav(path, wellname):
    """

    :param path: path of csv file
    :param well: well being searched
    :return: google maps link of well
    """
    df = pd.read_csv(path)
    # logging.debug('original df %s' % df.head(1))

    lat = df.loc[df['WellNumber'].str.lower() == wellname.lower(), 'Latitude'].to_string(index=False)
    long = df.loc[df['WellNumber'].str.lower() == wellname.lower(), 'Longitude'].to_string(index=False)
    latlong = '{0},{1}'.format(lat, long).lstrip()
    logging.debug('lat:%s' % latlong)

    maplink = urljoin('https://www.google.com/maps/dir/', '?api=1&destination={0}'.format(latlong))
    logging.debug('map link is %s' % maplink)

    return maplink


""" FLASK PORTION OF CODE """


app = Flask(__name__)

@app.route('/')
def hello():
    """Proof of life for testing. Is the server up?"""
    return "Hello Flask Well Finder!"

@app.route('/wellfinder/', methods=['GET', 'POST'])
def wellfinder():
    if request.method == 'GET':
        """First, serving input form as a webpage"""
        return render_template('wellfinder.html')
    else:
        """Otherwise this is a POST to call the imported function"""
        wellname = request.form['wellname']
        logging.debug('inputs: {}'.format(wellname))
        try:
            path = 'AllWells.csv'
            navresult = wellnav(path, wellname)
            if navresult == 'https://www.google.com/maps/dir/?api=1&destination=Series([], ),Series([], )':
                error = 'Invalid Well Name. Please try again!'
                return render_template('wellfinder.html', error=error)
            else:
                return render_template('results.html', navresult=navresult)
        except Exception as e:
            traceback.print_exc()
            abort(500, str(e))

if __name__ == '__main__':
    app.run()

