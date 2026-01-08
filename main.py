import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from interactive_cli import CLI
from edutrack_manager import EduTrackManager


def main():
 

    if len(sys.argv) > 1 and sys.argv[1] == '--populate':
    
        print("Attempting to populate sample data...")
        try:
            from populate_edutrack import populate_makini_school
            populate_makini_school()
            print("\nSample data population completed.")
        except ImportError:
            print("populate_edutrack module not found. Skipping population.")
        except Exception as e:
            print(f"Error during population: {e}")
    
    # Run interactive CLI
    try:
       
        print("Welcome to EduTrack - School Management System")
        
        cli = CLI()
        cli.run()
    except RuntimeError as e:
        # Catch MongoDB connection errors
        print(f"\n[ERROR] {e}")
        print("\nPlease configure your MongoDB connection:")
        print("  1. Set the EDUTRACK_MONGODB_URI environment variable, OR")
        print("  2. Create a config.json file with your MongoDB URI")
        print("\nSee config.example.json for the expected format.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nApplication terminated by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[FATAL ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
