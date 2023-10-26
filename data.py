from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# 업로드한 데이터를 저장할 데이터 프레임
data = None

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    global data
    if request.method == 'POST':
        file = request.files['file']
        if file:
            # 업로드한 파일을 데이터 프레임으로 읽기
            data = pd.read_csv(file)
            return redirect(url_for('dashboard'))

    return render_template('upload.html')

@app.route('/dashboard')
def dashboard():
    global data
    if data is None:
        return redirect(url_for('upload_file'))

    # 데이터 분석 및 시각화
    #
    # 이 예시에서는 간단한 히스토그램 생성
    plt.figure()
    data['Value'].plot(kind='hist')
    plt.title('Histogram of Values')
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    
    return render_template('dashboard.html', plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)
