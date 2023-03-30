import streamlit as st
import numpy as np
import pandas as pd
import pickle
import requests
from streamlit_lottie import st_lottie

def load_lottieURL(url):
    r = requests.get(url)
    if r.status_code != 200: # not succesful
        return None
    else: return r.json()
        
lottie_animation=load_lottieURL("https://assets1.lottiefiles.com/datafiles/HN7OcWNnoqje6iXIiZdWzKxvLIbfeCGTmvXmEm1h/data.json")

brand_dic = {'Datsun': 0, 'Force': 1, 'Ford': 2, 'Honda': 3, 'Hyundai': 4, 'Isuzu': 5, 'Jeep': 6, 'Kia': 7, 'MG': 8, 'Mahindra': 9, 'Maruti': 10, 'Nissan': 11, 'Renault': 12, 'Skoda': 13, 'Tata': 14, 'Toyota': 15, 'Volkswagen': 16}
model_dic = {'Alto': 0, 'Altroz': 1, 'Amaze': 2, 'Aspire': 3, 'Baleno': 4, 'Bolero': 5, 'Celerio': 6, 'Ciaz': 7, 'City': 8, 'Civic': 9, 'Compass': 10, 'Creta': 11, 'D-Max': 12, 'Duster': 13, 'Dzire LXI': 14, 'Dzire VXI': 15, 'Dzire ZXI': 16, 'Ecosport': 17, 'Eeco': 18, 'Elantra': 19, 'Ertiga': 20, 'Figo': 21, 'Freestyle': 22, 'GO': 23, 'Glanza': 24, 'Grand': 25, 'Gurkha': 26, 'Harrier': 27, 'Hector': 28, 'Hexa': 29, 'Ignis': 30, 'Innova': 31, 'Jazz': 32, 'KUV': 33, 'KUV100': 34, 'KWID': 35, 'Kicks': 36, 'Marazzo': 37, 'Nexon': 38, 'Polo': 39, 'Rapid': 40, 'RediGO': 41, 'S-Presso': 42, 'Safari': 43, 'Santro': 44, 'Scorpio': 45, 'Seltos': 46, 'Swift': 47, 'Swift Dzire': 48, 'Thar': 49, 'Tiago': 50, 'Tigor': 51, 'Triber': 52, 'Tucson': 53, 'Vento': 54, 'Venue': 55, 'Verna': 56, 'Vitara': 57, 'WR-V': 58, 'Wagon R': 59, 'X-Trail': 60, 'XL6': 61, 'XUV300': 62, 'XUV500': 63, 'Yaris': 64, 'i10': 65, 'i20': 66, 'redi-GO': 67}
seller_dic = {'Dealer': 0, 'Individual': 1, 'Trustmark Dealer': 2}
fuel_dic = {'CNG': 0, 'Diesel': 1, 'LPG': 2, 'Petrol': 3}
transmission_dic={'Automatic': 0, 'Manual': 1}

cars=pd.read_csv('final_carData.csv')
carsX=cars.drop(columns=['Unnamed: 0','selling_price'],axis=1)

st.set_page_config(page_title="Used Car Price Prediction",page_icon=":car:",layout='wide',initial_sidebar_state="expanded")
nav = st.sidebar.radio("**Navigation**",["Home","Prediction","About US"],index=0)

if nav == "Home":
    st.title("Used Car Price Prediction")
    st.subheader("Predict prices of your used cars for buying or selling")
    st.image('car1.jpg')

if nav == "Prediction":
    
    with st.spinner(":car: :car: Hold On,the predictor is loading!!... :car: :car: "):
        load_model=pickle.load(open('RF_car_pred_model','rb'))
        st.subheader("**:exclamation: Used Car Price Predictior :car: :exclamation:**")
    
    left_column,right_column = st.columns(2)
    
    with right_column:
        st_lottie(lottie_animation,height=500,key="car")
    
    with left_column:
        brand = st.selectbox('Select Brand : ', cars.brand.unique())
        model = st.selectbox('Select Model : ', cars[cars['brand']==brand].model.unique())
        age = st.number_input('Enter Age (yrs) : ',min_value=0,max_value=1000)
        km = st.number_input("Km's Driven : ")
        mileage = st.number_input("mileage(km/l) : ")
        engine = st.number_input("Engine (cc) : ")
        max_power = st.number_input("Max Power (hp) : ")
        seats = st.slider("No. of Seats : ",min_value=2,max_value=10)
        seller = st.selectbox('Seller : ', cars.seller_type.unique())
        fuel = st.selectbox('Fuel Type : ', cars.fuel_type.unique())
        transmission = st.selectbox('Transmission Type : ', cars.transmission_type.unique())
        costPrice = st.number_input("Cost price (lakhs) : ",min_value=0.0)

        brand_enc=brand_dic[brand]
        model_enc=model_dic[model]
        seller_type_enc=seller_dic[seller]
        fuel_type_enc=fuel_dic[fuel]
        transmission_type_enc=transmission_dic[transmission]

        featuers=pd.DataFrame.from_dict([{'vehicle_age':age, 'km_driven':km, 'mileage':mileage, 'engine':engine, 'max_power':max_power, 'seats':seats, 'avg_cost_price':costPrice, 'brand_enc':brand_enc ,'model_enc':model_enc, 'seller_type_enc':seller_type_enc, 'fuel_type_enc':fuel_type_enc, 'transmission_type_enc':transmission_type_enc}])
        featuers.info()
        
        if st.button("Predict Selling Price"):
            SP=load_model.predict(featuers)
            st.text_area("Selling Price (lakhs) : ", np.round(SP,2))
    
if nav == "About US":
    st.subheader("This project is created by :")
    st.write("### SHIVANSH TIWARI")
    st.caption("***Student at Jaypee University Of Engineering And Technology, Guna, Madhya Pradesh (2020 - 2024)***")
    

  
