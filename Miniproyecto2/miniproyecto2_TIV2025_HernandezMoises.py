# -*- coding: utf-8 -*-
"""
Created on Sat Jun 21 18:14:46 2025

@author: moymo
"""

import streamlit as st
import pandas as pd
import os

#Titulo de la pestaña del navegador
st.set_page_config(page_title="Gestión de Estudiantes", page_icon="🎓", layout="centered", 
                   initial_sidebar_state="expanded")

#Creacion de la clase
class AppEstudiantes:
    def __init__(self):
        self.archivo = "estudiantes.csv" 
        if os.path.exists(self.archivo):
            st.session_state.df = pd.read_csv(self.archivo)
            st.session_state.estudiantes = st.session_state.df.to_dict(orient="records")
        else:
            st.session_state.estudiantes = []
            st.session_state.df = pd.DataFrame()

    def vista_registro(self):
        st.title("📋 Registro de Estudiantes 📋")

        with st.form("formulario_estudiantes"):
            col1, col2 =st.columns(2)
            
            with col1:
                nombre = st.text_input("Nombre completo")
                edad = st.slider("Edad", min_value=16, max_value=99, value=18)
            
            with col2:
                opciones_carrera = ["--Selecciona una carrera--", "Ingeniería", "Psicología", "Diseño", "Arquitectura", "Medicina"]
                carrera  = st.selectbox("Carrera", opciones_carrera)
                regular = st.radio("¿Eres alumno regular?", ["Sí", "No"])
            enviar = st.form_submit_button("Guardar")

        if enviar:
            if not nombre:
                st.warning("⚠️ El nombre no puede estar vacío.")
                return
            if carrera == "--Selecciona una carrera--":
                st.warning("⚠️ Debes seleccionar una carrera valida")

            nuevo = {
                "Nombre": nombre,
                "Edad": edad,
                "Carrera": carrera,
                "Regular": regular
                }

            st.session_state.estudiantes.append(nuevo)
            st.session_state.df = pd.DataFrame(st.session_state.estudiantes)
            st.session_state.df.to_csv(self.archivo, index=False)

            st.success("✅ Estudiante registrado correctamente.")
            st.write("### Resumen del registro:")
            st.markdown(f"""
                        - **Nombre:** {nuevo["Nombre"]}
                        - **Edad:** {nuevo["Edad"]}
                        - **Carrera:** {nuevo["Carrera"]}
                        - **Alumno regular:** {nuevo["Regular"]}
                        """)
    def vista_consulta(self):
        st.title("🔍 Consulta de Estudiantes 🔍")
        df = st.session_state.df
        
        if df.empty:
            st.info("No existen estudiantes registrados.")
        else:
            st.subheader("Tabla de registros.")
            st.dataframe(df)
            
            st.subheader("📊 Gráfica de estudiantes por carrera 📊")
            carreras = df["Carrera"].unique().tolist()
            seleccionadas = st.multiselect("Selecciona carreras", carreras, default=carreras)

            df_filtrado = df[df["Carrera"].isin(seleccionadas)]
            conteo = df_filtrado["Carrera"].value_counts().reset_index()
            conteo.columns = ["Carrera", "Cantidad"]

            import plotly.express as px
            fig = px.bar(conteo, x="Carrera", y="Cantidad", color="Carrera", text="Cantidad",
                         title="Cantidad de estudiantes por carrera")
            st.plotly_chart(fig)

            st.subheader("📁 Exportar datos filtrados 📁")
            nombre_archivo = st.text_input("Nombre del archivo", value="reporte_estudiantes.csv")
            directorio = st.text_input("Ruta de carpeta destino", value=os.getcwd())
            
            if st.button("Exportar CSV"):
                ruta_completa = os.path.join(directorio, nombre_archivo)
                try:
                    df_filtrado.to_csv(ruta_completa, index=False)
                    st.success(f"✅ Archivo exportado en:\n`{ruta_completa}`")
                except Exception as e:
                    st.error(f"❌ Error al exportar el archivo:\n{e}")
    
    
    def run(self):
        st.sidebar.title("📚 Menú")
        opcion = st.sidebar.selectbox("Selecciona una sección", ["Registro", "Consulta y Gráfica"])

        if opcion == "Registro":
            self.vista_registro()
        elif opcion == "Consulta y Gráfica":
            self.vista_consulta()
# Ejecutar solo la parte 1
app = AppEstudiantes()
app.run()
            
    