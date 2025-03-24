# QR Code Generator

A comprehensive web application that allows users to generate, customize, manage, and share QR codes. Built with Django and enhanced with modern UI/UX design principles.

## Features

- **User Authentication**: Register, login, and manage your account
- **QR Code Generation**: Generate QR codes from any text or URL
- **Customization Options**: 
  - Choose foreground and background colors
  - Adjust QR code size and border
  - Name and organize your QR codes
- **Multiple Export Formats**: Download QR codes as PNG, SVG, or PDF
- **User Profile & Preferences**: 
  - View your QR code history
  - Set preferred language
  - Configure default QR code settings
- **Analytics**: Track views, downloads, and shares for your QR codes
- **RESTful API**: Programmatically generate and manage QR codes
- **Internationalization**: Multi-language support
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## Installation

1. Clone the repository to your local machine:

   ```
   git clone https://github.com/sobit-nep/QRCodeGenerator.git
   ```

2. Navigate to the project directory:

   ```
   cd Django-QRCodeGenerator-main
   ```

3. Create a virtual environment:

   ```
   python -m venv venv
   ```

4. Activate the virtual environment:

   - For Windows:

     ```
     venv\Scripts\activate
     ```

   - For macOS/Linux:

     ```
     source venv/bin/activate
     ```

5. Install the dependencies:

   ```
   pip install -r requirements.txt
   ```

6. Apply database migrations:

   ```
   python manage.py migrate
   ```

7. Run the development server:

   ```
   python manage.py runserver
   ```

8. Access the application in your web browser at `http://localhost:8000`.

## API Usage

The application provides a RESTful API for generating and managing QR codes programmatically:

1. Obtain an authentication token:
   ```
   POST /api-token-auth/
   {"username": "your_username", "password": "your_password"}
   ```

2. Generate a QR code:
   ```
   POST /api/generate-qr/
   Authorization: Token your_token
   {
     "content": "https://example.com",
     "name": "My Website",
     "foreground_color": "#000000",
     "background_color": "#FFFFFF",
     "box_size": 10,
     "border": 4
   }
   ```

3. Retrieve your QR codes:
   ```
   GET /api/qr-codes/
   Authorization: Token your_token
   ```

For complete API documentation, visit `/api/docs/` in the running application.

## Screenshots

![Home Page](https://github.com/sobit-nep/Django-QRCodeGenerator/assets/65544518/ca054874-11dd-4e2d-80f1-362acd0f1f6e)
![QR Detail](https://github.com/sobit-nep/Django-QRCodeGenerator/assets/65544518/ecd1e01d-4ff7-4bf0-85b9-b159cf456857)

## Contributing

Contributions are welcome! If you have any suggestions, improvements, or bug fixes, please submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
