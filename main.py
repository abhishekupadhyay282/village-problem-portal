#!/usr/bin/env python3
"""Main entry point for the Village Problem Portal."""

from app import create_app
import os

if __name__ == "__main__":
    app = create_app()
    
    # Get port from environment or use 8000 for local development
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    print("\n" + "="*60)
    print("🏘️  Village Problem Portal")
    print("="*60)
    print(f"\nStarting Flask server on port {port}...")
    print("Visit: http://localhost:" + str(port))
    print("Admin Dashboard: http://localhost:" + str(port) + "/admin")
    print("\nPress Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    app.run(debug=debug, host='0.0.0.0', port=port)
