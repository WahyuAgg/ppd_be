"""add_music_emotion_labels_table

Revision ID: 478724864acc
Revises: 864760f19b85
Create Date: 2025-12-17 13:35:10.201228

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '478724864acc'
down_revision: Union[str, Sequence[str], None] = '864760f19b85'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'music_emotion_labels',
        sa.Column('music_id', sa.Integer(), nullable=False),
        sa.Column('emotion_label_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['emotion_label_id'], ['emotion_labels.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['music_id'], ['musics.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('music_id', 'emotion_label_id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('music_emotion_labels')
