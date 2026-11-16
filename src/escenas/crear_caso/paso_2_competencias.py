# escenas/crear_caso/paso_2_competencias.py
import streamlit as st
from escenas.crear_caso.utils import (
    aplicar_css_panel, inicializar_caso, obtener_caso, actualizar_caso,
    ir_a_paso, cancelar_creacion, es_modo_editar,
    COMPETENCIAS
)

def mostrar():
    """Paso 2: Selección de competencias del perfil de egreso"""
    
    aplicar_css_panel()
    inicializar_caso()
    
    caso = obtener_caso()
    modo_editar = es_modo_editar()
    
    if not caso.get('nombre_caso'):
        st.warning("Debes completar el Paso 1 primero")
        if st.button("← Volver al Paso 1"):
            ir_a_paso(1)
        return
    
    col_cancelar, col_espacio = st.columns([1, 5])
    with col_cancelar:
        if st.button("← Cancelar", key="btn_cancelar_paso2", use_container_width=True):
            cancelar_creacion()
    
    titulo = "Editar Caso" if modo_editar else "Crear Caso Nuevo"
    st.markdown(f'<h1 class="medico-title">{titulo}</h1>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="info-paso">
        <strong>Paso 2 de 5:</strong> Competencias del Perfil de Egreso<br>
        <small>Caso: {caso.get('id_caso', '')} - {caso.get('nombre_caso', '')}</small>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background-color: #FFFFFF; padding: 15px; border-radius: 8px; border-left: 4px solid #70257E; margin-bottom: 1.5rem; color: #303442;">
        <strong>Instrucción:</strong> Selecciona las competencias del perfil de egreso que deseas evaluar en este caso. 
        Toma en cuenta que el escenario tiene una duración máxima de 10 minutos.
    </div>
    """, unsafe_allow_html=True)
    
    # ===== INICIALIZAR COMPETENCIAS SELECCIONADAS =====
    if 'competencias_seleccionadas' not in caso or caso['competencias_seleccionadas'] is None:
        actualizar_caso('competencias_seleccionadas', [])
        caso['competencias_seleccionadas'] = []
        
    # Hacemos una copia local para iterar y guardar
    competencias_actuales = caso.get('competencias_seleccionadas', []).copy()
    
    # Helper para verificar si una competencia ya está seleccionada
    def esta_seleccionada(cat_principal, subcat, texto_comp):
        for c in competencias_actuales:
            if (c.get('texto') == texto_comp and 
                c.get('categoria') == cat_principal and 
                c.get('subcategoria') == subcat):
                return True
        return False

    # ===== RENDERIZAR COMPETENCIAS POR CATEGORÍA =====
    for categoria_principal, subcategorias in COMPETENCIAS.items():
        st.markdown(f'<div class="section-title">{categoria_principal}</div>', unsafe_allow_html=True)
        
        for subcategoria, lista_competencias in subcategorias.items():
            with st.expander(f"📌 {subcategoria}", expanded=False):
                for comp in lista_competencias:
                    # Verificar si ya estaba seleccionada
                    valor_actual = esta_seleccionada(categoria_principal, subcategoria, comp)
                    
                    # Usamos una key única
                    key_checkbox = f"chk_{hash(categoria_principal+subcategoria+comp)}"
                    
                    # Renderizamos el checkbox
                    seleccionada_ahora = st.checkbox(
                        comp, 
                        value=valor_actual, 
                        key=key_checkbox
                    )
                    
                    # Lógica para actualizar la lista sin usar on_change
                    if seleccionada_ahora and not valor_actual:
                        # Se acaba de marcar -> Agregar
                        competencias_actuales.append({
                            "categoria": categoria_principal,
                            "subcategoria": subcategoria,
                            "texto": comp
                        })
                    elif not seleccionada_ahora and valor_actual:
                        # Se acaba de desmarcar -> Quitar
                        competencias_actuales = [c for c in competencias_actuales if not (
                            c.get('texto') == comp and 
                            c.get('categoria') == categoria_principal and 
                            c.get('subcategoria') == subcategoria
                        )]
    
    # Guardamos los cambios en el caso (siempre, para no perderlos)
    actualizar_caso('competencias_seleccionadas', competencias_actuales)

    st.markdown("---")
    
    # ===== BOTONES =====
    col_btn1, col_btn2, col_btn3 = st.columns([3, 1, 1])
    with col_btn2:
        if st.button("← Atrás", key="btn_atras_paso2", use_container_width=True):
            ir_a_paso(1)
            
    with col_btn3:
        with st.container(key="btn_siguiente_crear_caso"):
            if st.button("Siguiente →", key="btn_siguiente_paso2", use_container_width=True, type="primary"):
                ir_a_paso(3)