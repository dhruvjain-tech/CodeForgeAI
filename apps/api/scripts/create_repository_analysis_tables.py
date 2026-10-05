from database import Base, engine

import models.repository_analysis  # noqa: F401


def main() -> None:
    Base.metadata.create_all(bind=engine)

    print("Repository analysis tables created successfully.")


if __name__ == "__main__":
    main()