"""added images table and relationship to product

Revision ID: 26ef898ad515
Revises: a8ffbb56cfac
Create Date: 2023-08-16 18:21:00.183364

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26ef898ad515'
down_revision = 'a8ffbb56cfac'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('images',
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_images_id'), 'images', ['id'], unique=False)
    op.drop_column('products', 'img_url')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('img_url', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_images_id'), table_name='images')
    op.drop_table('images')
    # ### end Alembic commands ###
