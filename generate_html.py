def generate_html(results):
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Ofertas</title>
        <style>
            table {
                width: 100%;
                border-collapse: collapse;
            }
            th, td {
                padding: 8px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }
            th {
                background-color: #f2f2f2;
            }
            tr:hover {
                background-color: #f5f5f5;
            }
            .strikethrough {
                text-decoration: line-through;
            }
            img {
                width: 100px; /* Ajusta el tamaño de las imágenes */
                height: auto;
            }
            .no-image {
                width: 100px; /* Ajusta el tamaño de la X */
                height: 100px;
                display: block;
                background: url('x_image_path') center center no-repeat;
                background-size: contain;
            }
        </style>
    </head>
    <body>
        <h1>Ofertas</h1>
        <table>
            <tr>
                <th>Imagen</th>
                <th>Producto</th>
                <th>Precio</th>
                <th>Precio sin descuento</th>
                <th>Rebaja</th>
                <th>Enlace</th>
            </tr>
    """

    for result in results:
        img_tag = f'<img src="{result["Imagen"]}" alt="{result["Producto"]}">' if result["Imagen"] else '<div class="no-image"></div>'
        html_content += f"""
                    <tr>
                        <td>{img_tag}</td>
                        <td>{result['Producto']}</td>
                        <td>{result['Precio']}</td>
                        <td class="strikethrough">{result['Precio sin descuento']}</td>
                        <td>{result['Rebaja']}</td>
                        <td><a href="{result['Enlace']}">[link]</a></td>
                    </tr>
        """

    html_content += """
        </table>
    </body>
    </html>
    """

    with open('products.html', 'w', encoding='utf-8') as file:
        file.write(html_content)

    print(f"HTML file generated successfully.")

# Reemplaza 'x_image_path' con la ruta real de la imagen de X.
def update_x_image_path(x_image_path):
    with open('products.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    html_content = html_content.replace('x_image_path', x_image_path)

    with open('products.html', 'w', encoding='utf-8') as file:
        file.write(html_content)