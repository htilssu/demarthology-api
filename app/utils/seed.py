from logging import Logger

from app.models.role import Role

logger = Logger("seed")


async def seed_default_roles():
    """Seed default roles into the database."""
    try:
        # Check if roles already exist
        existing_roles = await Role.find_all().to_list()
        if existing_roles:
            logger.info(f"Roles already exist: {len(existing_roles)} roles found")
            return

        # Create default roles
        default_roles = [
            Role(name="user", description="Default user role"),
            Role(name="admin", description="Administrator role"),
            Role(name="moderator", description="Moderator role"),
        ]

        for role in default_roles:
            await role.create()
            logger.info(f"Created default role: {role.name}")

        logger.info("Default roles seeded successfully")
    except Exception as e:
        logger.error(f"Error seeding default roles: {str(e)}")
        raise
