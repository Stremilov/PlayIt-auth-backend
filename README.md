
# PlayIT dev branch

## How to start the Project

1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   cd <project_directory>
   ```

2. **Set Up a Virtual Environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Create and Configure `.env`:**
   - Copy the contents of `example.env` to a new file named `.env`:
     ```bash
     cp example.env .env
     ```
   - Fill in the required values in `.env` (e.g., database credentials).

4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Application:**
   ```bash
   cd src
   python main.py
---

## Summary of Work Done


### **Implemented Features**
1. **Migrated Models from Django ORM to SQLAlchemy (Synchronous):**
   - Rewrote all models to work with SQLAlchemy instead of Django ORM.
   - Synchronous database interactions are implemented for PostgreSQL.

2. **Set Up PostgreSQL Integration:**
   - Database setup is managed in `db/db.py`, including connection and table creation.

3. **Moved Enums to a Separate File:**
   - Moved `RoleEnum` and `StatusEnum` to `utils/enums.py` for better modularity and reusability.

4. **Created Pydantic Schemas:**
   - Designed schemas for `task` and `user` entities to handle data validation and serialization.

5. **Developed Repository and Service for User:**
   - Implemented methods in the repository and service layers:
     - `create_user`
     - `get_user_by_user_id`
     - `get_user_by_telegram_id`
     - `get_all_users`
     - `update_user_by_user_id`
     - `delete_user_by_user_id`

6. **Rewrote `telegram-login` Endpoint:**
   - Migrated the `telegram-login` functionality from Django to FastAPI.
   - The endpoint now uses SQLAlchemy for database interactions and Pydantic for response validation.

7. **Preserved Existing Session Logic:**
   - Moved the session handling logic from `main.py` into a separate directory for better modularity.
   - Updated session dependencies to integrate seamlessly with FastAPI.

8. **Implemented `get_user_role` Endpoint:**
   - Added functionality to retrieve a user's role in the `Users` service.
   - Integrated the endpoint with session validation and service logic.

9. **Updated Repository and Service Logic:**
   - Made adjustments to the repository and service layers for improved functionality and maintainability.

---

## Remaining Work

1. **Error Handling:**
   - Implement global and local error handling to improve the robustness of the application.

2. **Testing:**
   - Perform comprehensive testing of the endpoints, including edge cases and error scenarios.
