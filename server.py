import asyncio
import os

host_address = '127.0.0.1'
port_number = 8085

async def handle_client(reader, writer):
    request = await reader.read(1024)
    request = request.decode()

    if not request:
        writer.close()
        await writer.wait_closed()
        return

    line = request.split('\r\n')[0]
    method, path, _ = line.split(' ')

    if method == 'GET':
        if path == '/':
            await send_response_file(writer, 'templates/index.html')
        elif path == '/register':
            await send_response_file(writer, 'templates/register.html')
        elif path.startswith('/assets/'):
            await send_response_file(writer, path[1:], binary=True)
        else:
            await send_response_file(writer, 'templates/404.html')
    elif method == 'POST' and path == '/submit':
        data = request.split('\r\n\r\n')[1]
        form_data = {}
        for entry in data.split('&'):
            if '=' in entry:
                field_name, user_input = entry.split('=')
                form_data[field_name] = user_input

        user_name = form_data.get('username', '')
        email = form_data.get('email', '')

        if user_name and email:
            with open('db.txt', 'a') as file:
                file.write(user_name + ' ' + email + '\n')
            await send_html_page(writer, "<h1>Registration Successful</h1><a href='/'>Go Home</a>")
    else:
        await send_response_file(writer, 'templates/404.html')

    writer.close()
    await writer.wait_closed()

async def send_response_file(writer, file_name, binary=False):
    if not os.path.exists(file_name):
        file_name = 'templates/404.html'

    with open(file_name, 'rb' if binary else 'r') as file:
        content = file.read()

    writer.write(b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
    writer.write(content if binary else content.encode())
    await writer.drain()

async def send_html_page(writer, html):
    writer.write(b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
    writer.write(html.encode())
    await writer.drain()

async def main():
    server = await asyncio.start_server(handle_client, host_address, port_number)
    print(f"Server running at http://{host_address}:{port_number}")
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())
