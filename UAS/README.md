# UAS spk_web

## Install requirements

    pip install -r requirements.txt

## Run the app
to run the web app simply  use

    python main.py

## Usage
Install postman 
https://www.postman.com/downloads/

get cafe list
<img src='img/get_cafe.png' alt='cafe list'/>

get recommendations saw
<img src='img/post_saw.png' alt='recommendations saw'/>

get recommendations wp
<img src='img/post_wp.png' alt='recommendations wp'/>

### TUGAS UAS
Implementasikan model yang sudah anda buat ke dalam web api dengan http method `POST`

INPUT:
{
    'rating_minuman': 5, 
    'harga': 5, 
    'kualitas_pelayanan': 5, 
    'suasana': 5, 
    'rasa': 5
}
OUTPUT (diurutkan / sort dari yang terbesar ke yang terkecil):

post recommendations saw
<img src='img/post_saw.png' alt='recommendations saw'/>

post recommendations wp
<img src='img/post_wp.png' alt='recommendations wp'/>
