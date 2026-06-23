import os
import json
import pandas as pd

# Directorio actual
dir_actual = os.path.dirname(os.path.abspath(__file__))

# Rutas de archivos
ruta_csv = os.path.join(dir_actual, "customer_behavior_dataset_sin_outliers.csv")
ruta_txt = os.path.join(dir_actual, "descripcion_de_columnas.txt")
ruta_html = os.path.join(dir_actual, "visualizacion_tabla.html")

# 1. Cargar el dataset
if not os.path.exists(ruta_csv):
    print(f"Error: No se encontró el archivo '{ruta_csv}'.")
    exit(1)

df = pd.read_csv(ruta_csv)

# 2. Cargar y parsear las descripciones de columnas
column_mapping = {}
if os.path.exists(ruta_txt):
    with open(ruta_txt, "r", encoding="utf-8") as f:
        for line in f:
            if ":" in line:
                parts = line.split(":", 1)
                col_name = parts[0].strip()
                col_desc = parts[1].strip()
                # Limpiar el punto final si existe
                if col_desc.endswith("."):
                    col_desc = col_desc[:-1]
                column_mapping[col_name] = col_desc
else:
    print(f"Advertencia: No se encontró '{ruta_txt}'. Se usarán los nombres por defecto.")

# Caso especial para la columna creada dinámicamente
if 'Edad' not in column_mapping:
    column_mapping['Edad'] = 'Edad del cliente'

# Filtrar mapeo para las columnas que realmente existen en el dataset
columnas_existentes_mapeadas = {}
for col in df.columns:
    if col in column_mapping:
        # Simplificar descripciones extremadamente largas para los encabezados de la tabla
        desc = column_mapping[col]
        # Si la descripción es muy larga, la acortamos un poco para los headers, pero la dejamos descriptiva
        if len(desc) > 50:
            if "1 si el cliente" in desc:
                # Ejemplo: "1 si el cliente realizó una queja en los últimos 2 años, 0 en caso contrario"
                # -> "Queja realizada (últimos 2 años)"
                desc = desc.replace("1 si el cliente ", "").replace(", 0 en caso contrario", "").capitalize()
            elif "1 si el cliente aceptó la oferta" in desc:
                # -> "Aceptó oferta en campaña X"
                desc = desc.replace("1 si el cliente aceptó la oferta en la ", "Aceptó oferta en ").replace(", 0 en caso contrario", "").capitalize()
        columnas_existentes_mapeadas[col] = desc
    else:
        columnas_existentes_mapeadas[col] = col

# Renombrar columnas en el DataFrame
df_renombrado = df.rename(columns=columnas_existentes_mapeadas)

# 3. Calcular métricas para el panel resumen
total_registros = len(df_renombrado)
total_columnas = len(df_renombrado.columns)

col_ingreso_desc = columnas_existentes_mapeadas.get('Income', 'Income')
ingreso_promedio = f"${df_renombrado[col_ingreso_desc].mean():,.2f}" if col_ingreso_desc in df_renombrado.columns else "N/A"

col_edad_desc = columnas_existentes_mapeadas.get('Edad', 'Edad')
edad_promedio = f"{df_renombrado[col_edad_desc].mean():.1f} años" if col_edad_desc in df_renombrado.columns else "N/A"

# 4. Convertir datos a JSON
datos_json = df_renombrado.to_json(orient="records", force_ascii=False)
columnas_lista = list(df_renombrado.columns)

# 5. Generar archivo HTML interactivo premium
html_template = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visualización del Dataset de Clientes (Sin Outliers)</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #0b0f19;
            --card-bg: rgba(20, 26, 43, 0.65);
            --border-color: rgba(255, 255, 255, 0.08);
            --accent-gradient: linear-gradient(135deg, #3b82f6, #8b5cf6);
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
            --input-bg: #111827;
            --input-border: #374151;
            --input-focus: #3b82f6;
            --row-hover: rgba(255, 255, 255, 0.03);
            --badge-yes-bg: rgba(16, 185, 129, 0.15);
            --badge-yes-text: #10b981;
            --badge-yes-border: rgba(16, 185, 129, 0.3);
            --badge-no-bg: rgba(244, 63, 94, 0.1);
            --badge-no-text: #f43f5e;
            --badge-no-border: rgba(244, 63, 94, 0.2);
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Outfit', sans-serif;
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.12) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(139, 92, 246, 0.1) 0px, transparent 50%);
            background-attachment: fixed;
            color: var(--text-main);
            min-height: 100vh;
            padding: 2.5rem 1.5rem;
            line-height: 1.5;
        }}

        .container {{
            max-width: 1600px;
            margin: 0 auto;
        }}

        header {{
            margin-bottom: 2rem;
            position: relative;
        }}

        h1 {{
            font-size: 2.25rem;
            font-weight: 700;
            background: var(--accent-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
            display: inline-block;
        }}

        .subtitle {{
            color: var(--text-muted);
            font-size: 1rem;
        }}

        /* Panel de Métricas */
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}

        .metric-card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 1.25rem;
            backdrop-filter: blur(16px);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
            transition: transform 0.3s ease, border-color 0.3s ease;
        }}

        .metric-card:hover {{
            transform: translateY(-4px);
            border-color: rgba(139, 92, 246, 0.3);
        }}

        .metric-title {{
            font-size: 0.875rem;
            color: var(--text-muted);
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }}

        .metric-value {{
            font-size: 1.75rem;
            font-weight: 700;
            background: var(--accent-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        /* Filtros y Controles */
        .controls-card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            backdrop-filter: blur(16px);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
            display: flex;
            flex-wrap: wrap;
            gap: 1.5rem;
            align-items: center;
            justify-content: space-between;
        }}

        .search-wrapper {{
            position: relative;
            flex: 1;
            min-width: 280px;
            max-width: 450px;
        }}

        .search-input {{
            width: 100%;
            padding: 0.75rem 1rem 0.75rem 2.75rem;
            background: var(--input-bg);
            border: 1px solid var(--input-border);
            border-radius: 10px;
            color: var(--text-main);
            font-family: inherit;
            font-size: 0.95rem;
            transition: all 0.3s ease;
        }}

        .search-input:focus {{
            outline: none;
            border-color: var(--input-focus);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
        }}

        .search-icon {{
            position: absolute;
            left: 1rem;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            pointer-events: none;
            width: 16px;
            height: 16px;
        }}

        .filter-group {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}

        label {{
            font-size: 0.9rem;
            color: var(--text-muted);
        }}

        select {{
            padding: 0.6rem 2rem 0.6rem 1rem;
            background: var(--input-bg);
            border: 1px solid var(--input-border);
            border-radius: 8px;
            color: var(--text-main);
            font-family: inherit;
            font-size: 0.9rem;
            cursor: pointer;
            outline: none;
            appearance: none;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%239ca3af'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'/%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: right 0.75rem center;
            background-size: 1rem;
        }}

        select:focus {{
            border-color: var(--input-focus);
        }}

        .scroll-tip {{
            font-size: 0.85rem;
            color: #8b5cf6;
            display: flex;
            align-items: center;
            gap: 0.25rem;
            font-weight: 500;
        }}

        /* Tabla Contenedor */
        .table-card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
            margin-bottom: 1.5rem;
            backdrop-filter: blur(16px);
        }}

        .table-responsive {{
            overflow-x: auto;
            max-height: 60vh;
        }}

        /* Estilización de Scrollbars */
        .table-responsive::-webkit-scrollbar {{
            height: 10px;
            width: 10px;
        }}
        .table-responsive::-webkit-scrollbar-track {{
            background: rgba(0, 0, 0, 0.1);
        }}
        .table-responsive::-webkit-scrollbar-thumb {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
        }}
        .table-responsive::-webkit-scrollbar-thumb:hover {{
            background: rgba(255, 255, 255, 0.2);
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9rem;
            text-align: left;
        }}

        th {{
            background: rgba(17, 24, 39, 0.8);
            position: sticky;
            top: 0;
            z-index: 10;
            padding: 1rem 1.25rem;
            font-weight: 600;
            color: var(--text-main);
            border-bottom: 2px solid var(--border-color);
            white-space: nowrap;
            cursor: pointer;
            user-select: none;
            transition: background 0.2s ease;
        }}

        th:hover {{
            background: rgba(31, 41, 55, 0.9);
        }}

        .sort-icon {{
            display: inline-block;
            margin-left: 0.5rem;
            width: 12px;
            height: 12px;
            color: var(--text-muted);
            transition: transform 0.2s;
        }}

        td {{
            padding: 0.9rem 1.25rem;
            border-bottom: 1px solid var(--border-color);
            color: var(--text-muted);
            white-space: nowrap;
            font-weight: 400;
        }}

        tr:hover td {{
            color: var(--text-main);
            background-color: var(--row-hover);
        }}

        /* Primera columna fija para ID */
        th:first-child, td:first-child {{
            font-weight: 600;
            color: var(--text-main);
        }}

        /* Badges de respuesta y campañas */
        .badge {{
            display: inline-flex;
            align-items: center;
            padding: 0.25rem 0.6rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }}

        .badge-yes {{
            background-color: var(--badge-yes-bg);
            color: var(--badge-yes-text);
            border: 1px solid var(--badge-yes-border);
        }}

        .badge-no {{
            background-color: var(--badge-no-bg);
            color: var(--badge-no-text);
            border: 1px solid var(--badge-no-border);
        }}

        /* Paginación */
        .pagination-container {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 1rem;
            padding: 1.25rem;
            background: rgba(17, 24, 39, 0.4);
            border-top: 1px solid var(--border-color);
        }}

        .pagination-info {{
            font-size: 0.875rem;
            color: var(--text-muted);
        }}

        .pagination-buttons {{
            display: flex;
            gap: 0.5rem;
        }}

        .page-btn {{
            padding: 0.5rem 0.85rem;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            color: var(--text-main);
            font-family: inherit;
            font-size: 0.85rem;
            cursor: pointer;
            transition: all 0.2s ease;
            font-weight: 500;
        }}

        .page-btn:hover:not(:disabled) {{
            background: var(--accent-gradient);
            border-color: transparent;
            box-shadow: 0 0 10px rgba(139, 92, 246, 0.3);
        }}

        .page-btn:disabled {{
            opacity: 0.35;
            cursor: not-allowed;
        }}

        .page-btn.active {{
            background: var(--accent-gradient);
            border-color: transparent;
            font-weight: 600;
        }}

        /* Mensaje de no resultados */
        .no-results {{
            padding: 3rem;
            text-align: center;
            color: var(--text-muted);
            font-size: 1.1rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Dataset de Clientes Limpio (Sin Outliers)</h1>
            <div class="subtitle">Datos descriptivos y unificados según la especificación del proyecto</div>
        </header>

        <!-- Panel de Métricas Rápidas -->
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-title">Clientes Registrados</div>
                <div class="metric-value" id="metric-total-rows">{total_registros}</div>
            </div>
            <div class="metric-card">
                <div class="metric-title">Variables / Columnas</div>
                <div class="metric-value">{total_columnas}</div>
            </div>
            <div class="metric-card">
                <div class="metric-title">Ingreso Promedio</div>
                <div class="metric-value">{ingreso_promedio}</div>
            </div>
            <div class="metric-card">
                <div class="metric-title">Edad Promedio</div>
                <div class="metric-value">{edad_promedio}</div>
            </div>
        </div>

        <!-- Controles de búsqueda y filtros -->
        <div class="controls-card">
            <div class="search-wrapper">
                <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <input type="text" id="search-input" class="search-input" placeholder="Buscar por ID, educación, estado civil...">
            </div>

            <div class="filter-group">
                <label for="page-size">Mostrar:</label>
                <select id="page-size">
                    <option value="10">10 filas</option>
                    <option value="25" selected>25 filas</option>
                    <option value="50">50 filas</option>
                    <option value="100">100 filas</option>
                </select>
                
                <span class="scroll-tip">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                    Desliza horizontal para ver más columnas
                </span>
            </div>
        </div>

        <!-- Tabla -->
        <div class="table-card">
            <div class="table-responsive">
                <table id="data-table">
                    <thead>
                        <tr id="table-headers"></tr>
                    </thead>
                    <tbody id="table-body"></tbody>
                </table>
                <div id="no-results-msg" class="no-results" style="display: none;">
                    No se encontraron clientes que coincidan con la búsqueda.
                </div>
            </div>

            <!-- Paginación -->
            <div class="pagination-container">
                <div class="pagination-info" id="pagination-info"></div>
                <div class="pagination-buttons" id="pagination-buttons"></div>
            </div>
        </div>
    </div>

    <script>
        // Carga de datos crudos del dataset incrustado
        const rawData = {datos_json};
        const columns = {json.dumps(columnas_lista, ensure_ascii=False)};

        // Variables de estado
        let data = [...rawData];
        let filteredData = [...rawData];
        let currentPage = 1;
        let pageSize = 25;
        let sortColumn = null;
        let sortDirection = 'asc';
        let searchTerm = '';

        // Inicialización
        document.addEventListener('DOMContentLoaded', () => {{
            setupHeaders();
            setupEventListeners();
            updateTable();
        }});

        // Renderizar encabezados de columna de la tabla
        function setupHeaders() {{
            const headersRow = document.getElementById('table-headers');
            headersRow.innerHTML = '';
            
            columns.forEach(col => {{
                const th = document.createElement('th');
                th.innerHTML = `${{col}} <span class="sort-icon" id="sort-icon-${{col}}">↕</span>`;
                th.addEventListener('click', () => handleSort(col));
                headersRow.appendChild(th);
            }});
        }}

        // Configuración de listeners de inputs
        function setupEventListeners() {{
            // Búsqueda
            const searchInput = document.getElementById('search-input');
            searchInput.addEventListener('input', (e) => {{
                searchTerm = e.target.value.toLowerCase();
                currentPage = 1; // resetear a página 1
                filterAndSortData();
            }});

            // Cantidad de elementos por página
            const pageSizeSelect = document.getElementById('page-size');
            pageSizeSelect.addEventListener('change', (e) => {{
                pageSize = parseInt(e.target.value);
                currentPage = 1;
                updateTable();
            }});
        }}

        // Manejar el ordenamiento al hacer clic en columnas
        function handleSort(column) {{
            if (sortColumn === column) {{
                // Alternar dirección
                sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
            }} else {{
                sortColumn = column;
                sortDirection = 'asc';
            }}
            
            // Actualizar íconos visuales de ordenamiento
            columns.forEach(col => {{
                const icon = document.getElementById(`sort-icon-${{col}}`);
                if (col === column) {{
                    icon.innerHTML = sortDirection === 'asc' ? '▲' : '▼';
                    icon.style.color = '#3b82f6';
                }} else {{
                    icon.innerHTML = '↕';
                    icon.style.color = 'var(--text-muted)';
                }}
            }});

            filterAndSortData();
        }}

        // Filtrar y ordenar la lista globalmente
        function filterAndSortData() {{
            // 1. Filtrado
            if (searchTerm.trim() === '') {{
                filteredData = [...rawData];
            }} else {{
                filteredData = rawData.filter(row => {{
                    return columns.some(col => {{
                        const val = row[col];
                        if (val === null || val === undefined) return false;
                        return String(val).toLowerCase().includes(searchTerm);
                    }});
                }});
            }}

            // Actualizar contador rápido de filas filtradas
            document.getElementById('metric-total-rows').textContent = filteredData.length;

            // 2. Ordenamiento
            if (sortColumn) {{
                filteredData.sort((a, b) => {{
                    let valA = a[sortColumn];
                    let valB = b[sortColumn];

                    if (valA === null || valA === undefined) valA = '';
                    if (valB === null || valB === undefined) valB = '';

                    // Comprobar si son numéricos
                    const numA = Number(valA);
                    const numB = Number(valB);
                    
                    if (!isNaN(numA) && !isNaN(numB) && valA !== '' && valB !== '') {{
                        return sortDirection === 'asc' ? numA - numB : numB - numA;
                    }}

                    // Ordenamiento lexicográfico para texto
                    const strA = String(valA).toLowerCase();
                    const strB = String(valB).toLowerCase();
                    if (strA < strB) return sortDirection === 'asc' ? -1 : 1;
                    if (strA > strB) return sortDirection === 'asc' ? 1 : -1;
                    return 0;
                }});
            }}

            updateTable();
        }}

        // Renderizar el cuerpo de la tabla y paginador
        function updateTable() {{
            const tbody = document.getElementById('table-body');
            const noResults = document.getElementById('no-results-msg');
            tbody.innerHTML = '';

            const total = filteredData.length;

            if (total === 0) {{
                noResults.style.display = 'block';
                document.getElementById('pagination-info').textContent = 'Mostrando 0 de 0 registros';
                document.getElementById('pagination-buttons').innerHTML = '';
                return;
            }}
            noResults.style.display = 'none';

            // Paginación matemática
            const totalPages = Math.ceil(total / pageSize);
            if (currentPage > totalPages) currentPage = totalPages;
            if (currentPage < 1) currentPage = 1;

            const startIndex = (currentPage - 1) * pageSize;
            const endIndex = Math.min(startIndex + pageSize, total);
            const pageData = filteredData.slice(startIndex, endIndex);

            // Generar filas
            pageData.forEach(row => {{
                const tr = document.createElement('tr');
                
                columns.forEach(col => {{
                    const td = document.createElement('td');
                    let val = row[col];
                    
                    // Tratamiento visual de valores
                    if (val === null || val === undefined) {{
                        td.innerHTML = '<span style="color: rgba(255,255,255,0.15)">-</span>';
                    }} else if (col.toLowerCase().includes('campaña') || col.toLowerCase().includes('queja') || col.toLowerCase().includes('response') || col.toLowerCase().includes('complain') || col.toLowerCase().includes('aceptó')) {{
                        // Mostrar lindos badges para valores binarios (1 / 0)
                        if (val == 1) {{
                            td.innerHTML = '<span class="badge badge-yes">Sí (1)</span>';
                        }} else if (val == 0) {{
                            td.innerHTML = '<span class="badge badge-no">No (0)</span>';
                        }} else {{
                            td.textContent = val;
                        }}
                    }} else if (col.toLowerCase().includes('ingreso') || col.toLowerCase().includes('income') || col.toLowerCase().includes('monto') || col.toLowerCase().includes('gasto')) {{
                        // Formatear montos monetarios
                        const numVal = Number(val);
                        if (!isNaN(numVal)) {{
                            td.textContent = `$${{numVal.toLocaleString('es-ES', {{minimumFractionDigits: 0, maximumFractionDigits: 2}})}}`;
                            td.style.fontFamily = 'monospace';
                            td.style.fontWeight = '500';
                            td.style.color = '#3b82f6';
                        }} else {{
                            td.textContent = val;
                        }}
                    }} else if (typeof val === 'number') {{
                        td.textContent = val.toLocaleString('es-ES');
                    }} else {{
                        td.textContent = val;
                    }}
                    
                    tr.appendChild(td);
                }});
                tbody.appendChild(tr);
            }});

            // Info de paginación
            document.getElementById('pagination-info').textContent = `Mostrando ${{startIndex + 1}} a ${{endIndex}} de ${{total}} registros`;

            // Botones de paginación
            renderPaginationButtons(totalPages);
        }}

        // Renderizar botones numéricos del paginador
        function renderPaginationButtons(totalPages) {{
            const container = document.getElementById('pagination-buttons');
            container.innerHTML = '';

            // Botón Anterior
            const prevBtn = document.createElement('button');
            prevBtn.className = 'page-btn';
            prevBtn.textContent = '◀';
            prevBtn.disabled = currentPage === 1;
            prevBtn.addEventListener('click', () => {{
                currentPage--;
                updateTable();
            }});
            container.appendChild(prevBtn);

            // Páginas dinámicas simplificadas
            let startPage = Math.max(1, currentPage - 2);
            let endPage = Math.min(totalPages, startPage + 4);
            if (endPage - startPage < 4) {{
                startPage = Math.max(1, endPage - 4);
            }}

            for (let i = startPage; i <= endPage; i++) {{
                const pageBtn = document.createElement('button');
                pageBtn.className = `page-btn ${{i === currentPage ? 'active' : ''}}`;
                pageBtn.textContent = i;
                pageBtn.addEventListener('click', () => {{
                    currentPage = i;
                    updateTable();
                }});
                container.appendChild(pageBtn);
            }}

            // Botón Siguiente
            const nextBtn = document.createElement('button');
            nextBtn.className = 'page-btn';
            nextBtn.textContent = '▶';
            nextBtn.disabled = currentPage === totalPages;
            nextBtn.addEventListener('click', () => {{
                currentPage++;
                updateTable();
            }});
            container.appendChild(nextBtn);
        }}
    </script>
</body>
</html>
"""

# 6. Escribir el archivo HTML final
with open(ruta_html, "w", encoding="utf-8") as f:
    f.write(html_template)

print(f"¡Éxito! Archivo de visualización interactivo generado en: {ruta_html}")
