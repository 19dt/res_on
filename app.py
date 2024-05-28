import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import re
import uuid
from google_sheet import GoogleSheet
import numpy as np
import datetime as dt

from send_email import send
from google_calendar import GoogleCalendar


api_whatsapp= "https://api.whatsapp.com/send?phone=34667963510&text=YOUR_TEXT"
# VARIABLES

page_title = "JCA Barber"
page_icon = "💈"
layout = "centered"
horas =["9:00","10:00","11:00"]

corte = ["Corte - 10€", "Corte + barba - 15€", "Corte + lavado - 16€"]
image = "assets/pel.jpeg"
image_maps =  Image.open("assets/maps.png")

document = "gestion_barber"
sheet = "reservas"
credentials = st.secrets["sheets"]["credentials_sheet"]
idcalendar = "jcabarbershop1@gmail.com"
time_zone = 'Europe/Madrid'

# Funcion con re
def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email):
        return True
    else:
        return False


def generate_uuid():
    return str(uuid.uuid4())

def add_hour_and_half(time):
    parsed_time = dt.datetime.strptime(time, "%H:%M").time()
    new_time = (dt.datetime.combine(dt.date.today(), parsed_time) + dt.timedelta(hours=1, minutes=30)).time()
    return new_time.strftime("%H:%M")

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)

st.image(image)
st.title("JCA Barber")
st.text("Calle Numancia 12")

selected = option_menu(menu_title=None, options=["Servicios", "Diseños", "Detalles", "Reseñas"], 
        icons=["scissors", "person-workspace","person-circle","bookmark"], orientation="horizontal")

if selected == "Detalles":
    
    
    st.subheader("Ubicación")
    st.markdown("""<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3131.1540052457226!2d-5.2681529236768165!3d38.29909948178364!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xd13444518f19131%3A0x2231cd8dd82df493!2sJose%20Carlos%20Barber%20Shop!5e0!3m2!1ses!2ses!4v1716884259741!5m2!1ses!2ses" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>""", unsafe_allow_html=True)
    
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
    if fecha:
        calendar = GoogleCalendar(credentials, idcalendar )
        hours_blocked = calendar.get_event_start_time(str(fecha))
        result_hours = np.setdiff1d(horas, hours_blocked)
        
    hora = c2.selectbox("Hora*", result_hours)
    tipo_corte = c1.selectbox("Tipo de corte*", corte)
    notas = c2.text_area("Notas")
    
    enviar = st.button("Reservar") 
    
    # Back
    if enviar:
        with st.spinner("Cargando...."):
            if nombre == "":
                st.warning("El campo nombre es obligatorio")
            elif email == "":
                st.warning("El campo email es obligatorio")
    
            elif not validate_email(email):
                st.warning("El email no es valido")
        
            else:
                #Crear evento en google calendar
                parsed_time = dt.datetime.strptime(hora, "%H:%M").time()
                hours1 = parsed_time.hour
                minutes1 = parsed_time.minute
                end_hours = add_hour_and_half(hora)
                parsed_time2 = dt.datetime.strptime(end_hours, "%H:%M").time()
                hours2 = parsed_time2.hour
                minutes2 = parsed_time2.minute
                start_time = dt.datetime(fecha.year, fecha.month, fecha.day, hours1, minutes1).astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
                end_time = dt.datetime(fecha.year, fecha.month, fecha.day, hours2, minutes2).astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
                calendar = GoogleCalendar(credentials, idcalendar)
                calendar.create_event(nombre, start_time, end_time, time_zone)
                # Crear registo en google sheet
                uid = generate_uuid()
                data = [[nombre, email, tipo_corte, str(fecha), hora, notas,uid]]
                gs = GoogleSheet(credentials, document, sheet)
                range = gs.get_last_row_range()
                gs.write_data(range, data)
                # Enviar email de confirmacion al usuario
                #send(email, nombre, fecha, hora, tipo_corte)
            
                st.success("Su cita ha sido reservada de forma exitosa.")
            
            