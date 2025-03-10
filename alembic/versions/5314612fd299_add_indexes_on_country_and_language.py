"""Add indexes on country and language

Revision ID: 5314612fd299
Revises: 1a5041499d7f
Create Date: 2024-12-28 19:50:01.902296

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5314612fd299'
down_revision: Union[str, None] = '1a5041499d7f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('idx_album_language', 'albums', ['language'], unique=False)
    op.create_index('idx_artist_country', 'artists', ['country'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_artist_country', table_name='artists')
    op.drop_index('idx_album_language', table_name='albums')
    # ### end Alembic commands ###
