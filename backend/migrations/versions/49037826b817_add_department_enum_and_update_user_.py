"""Add Department enum and update User model

Revision ID: 49037826b817
Revises: 73c5137d660e
Create Date: 2025-09-26 12:29:57.046912

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '49037826b817'
down_revision: Union[str, Sequence[str], None] = '73c5137d660e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create the enum type
    department_enum = sa.Enum('FIELD', 'WAREHOUSE', name='department')
    department_enum.create(op.get_bind(), checkfirst=True)
    
    # Add a temporary column to hold the enum values
    op.add_column('users', sa.Column('department_new', department_enum, nullable=True))
    
    # Convert existing string values to enum values
    # This assumes existing values are either 'Field' or 'Warehouse'
    op.execute("""
        UPDATE users 
        SET department_new = 
            CASE 
                WHEN LOWER(TRIM(department)) = 'field' THEN 'FIELD'::department
                WHEN LOWER(TRIM(department)) = 'warehouse' THEN 'WAREHOUSE'::department
                ELSE 'WAREHOUSE'::department  -- Default value if no match
            END
    """)
    
    # Drop the old column and rename the new one
    op.drop_column('users', 'department')
    op.alter_column('users', 'department_new', new_column_name='department', nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Add a temporary text column
    op.add_column('users', sa.Column('department_old', sa.String(), nullable=True))
    
    # Convert enum values back to strings
    op.execute("""
        UPDATE users 
        SET department_old = 
            CASE 
                WHEN department = 'FIELD' THEN 'Field'
                WHEN department = 'WAREHOUSE' THEN 'Warehouse'
                ELSE 'Warehouse'  -- Default value if no match
            END
    """)
    
    # Drop the enum column and rename the text column
    op.drop_column('users', 'department')
    op.alter_column('users', 'department_old', new_column_name='department', nullable=False)
    
    # Drop the enum type
    sa.Enum(name='department').drop(op.get_bind(), checkfirst=True)
