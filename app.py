from flask import Flask, render_template, request
import ee

# تهيئة Earth Engine
ee.Initialize()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    lat = float(request.form['lat'])
    lng = float(request.form['lng'])

    point = ee.Geometry.Point([lng, lat])

    # تواريخ المقارنة
    date_before = '2022-10-15'
    date_after = '2024-03-01'

    # جلب صورة قبل
    img_before = ee.ImageCollection('COPERNICUS/S2')\
        .filterBounds(point)\
        .filterDate(date_before, '2022-11-15')\
        .sort('CLOUDY_PIXEL_PERCENTAGE')\
        .first()

    # جلب صورة بعد
    img_after = ee.ImageCollection('COPERNICUS/S2')\
        .filterBounds(point)\
        .filterDate(date_after, '2024-04-01')\
        .sort('CLOUDY_PIXEL_PERCENTAGE')\
        .first()

    url_before = img_before.getThumbURL({
        'dimensions': 256,
        'region': point.buffer(50).bounds().getInfo(),
        'format': 'png'
    })

    url_after = img_after.getThumbURL({
        'dimensions': 256,
        'region': point.buffer(50).bounds().getInfo(),
        'format': 'png'
    })

    return render_template('result.html', lat=lat, lng=lng,
                           before_img=url_before, after_img=url_after)

if __name__ == '__main__':
    app.run(debug=True)
