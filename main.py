import sys
import logging
from config import Config
from planetary_viewer import PlanetaryViewer

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    try:
        config = Config()
        logger.info("Configuration loaded successfully.")
        
        viewer = PlanetaryViewer(config)
        logger.info("Planetary Viewer initialized. Starting application...")
        
        viewer.run()
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()