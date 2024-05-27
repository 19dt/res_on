import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import urllib.parse

api_whatsapp= "https://api.whatsapp.com/send?phone=34667963510&text=YOUR_TEXT"
# VARIABLES

page_title = "JCA Barber"
page_icon = "💈"
layout = "centered"
horas =["9:00","10:00","11:00"]
corte = ["Corte: 10€", "Corte + barba: 12€", "Corte + lavado: 15€"]
image = "assets/pel.jpeg"
image_maps =  Image.open("assets/maps.png")

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)

st.image(image)
st.title("JCA Barber")
st.text("Calle Numancia 12")

selected = option_menu(menu_title=None, options=["Servicios", "Diseños", "Detalles", "Reseñas"], 
        icons=["scissors", "person-workspace","person-circle","bookmark"], orientation="horizontal")

if selected == "Detalles":
    
    st.image("assets/maps.png")
    st.markdown("Pulsa [aqui](https://www.google.com/maps/place/Jose+Carlos+Barber+Shop/@38.2990953,-5.265578,17z/data=!3m1!4b1!4m6!3m5!1s0xd13444518f19131:0x2231cd8dd82df493!8m2!3d38.2990953!4d-5.265578!16s%2Fg%2F11clym3zq7?entry=ttu) para ver la dirección")
    
    st.subheader("Horarios")
    dia, hora = st.columns(2)

    
    dia.text("Lunes")
    hora.text("9:30 - 14:00 | 17:00 - 21:00")
    dia.text("Martes")
    hora.text("9:30 - 14:00 | 17:00 - 21:00")
    dia.text("Miercoles")
    hora.text("9:30 - 14:00 | 17:00 - 21:00")
    dia.text("Jueves")
    hora.text("9:30 - 14:00 | 17:00 - 21:00")
    dia.text("Viernes")
    hora.text("9:30 - 14:00 | 17:00 - 21:00")
    dia.text("Sabado")
    hora.text("9:30 - 14:00 | 17:00 - 21:00")
    
    st.subheader("Contacto")
    st.text("📞 662014283")
    phone_number = "34667963510"
    whatsapp_url = f"https://wa.me/{phone_number}"
    st.markdown(f"[Contactar por WhatsApp]({whatsapp_url})")
    
    st.subheader("Instagram")
    st.markdown("Siguenos [aqui](https://www.instagram.com/jca_barbershop/) en instagram")
    
if selected == "Diseños":
    
    st.write("##")
    st.image("assets/pelado1.jpg", caption="Muestra de diseño")
    st.write("#")
    st.image("assets/pelado2.jpg", caption="Muestra de diseño")
    st.write("#")
    st.image("assets/pelado3.jpg", caption="Muestra de diseño")

if selected == "Servicios":
    
    st.subheader("Reservar cita")
    c1,c2 = st.columns(2)
    nombre = c1.text_input("Tu nombre*", placeholder="Nombre*", label_visibility="hidden")
    email = c2.text_input("Tu email*", placeholder="Email*", label_visibility="hidden")
    fecha = c1.date_input("Fecha*")
    hora = c2.selectbox("Hora*", horas)
    tipo_corte = c1.selectbox("Tipo de corte*", corte)
    notas = c2.text_area("Notas")
    
    enviar = st.button("Reservar")
    
    
    # Back
    if enviar:
        if nombre == "":
            st.warning("El campo nombre es obligatorio")
        elif email == "":
            st.warning("El campo email es obligatorio")
            
        else:
            
            #Crear evento en google calendar
            # Crear registo en google sheet
            # Enviar email de confirmacion al usuario
            
            st.success("Su cita ha sido reservada de forma exitosa.")
            
            