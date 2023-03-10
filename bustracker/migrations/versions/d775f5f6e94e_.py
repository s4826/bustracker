"""empty message

Revision ID: d775f5f6e94e
Revises: 4b70efe62dfd
Create Date: 2023-02-14 19:45:35.259161

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "d775f5f6e94e"
down_revision = "4b70efe62dfd"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("_alembic_tmp_users")
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_column("password")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("password", sa.VARCHAR(length=128), nullable=True)
        )

    op.create_table(
        "_alembic_tmp_users",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("email", sa.VARCHAR(length=64), nullable=True),
        sa.Column("pw_hash", sa.VARCHAR(length=128), nullable=True),
        sa.Column("confirmed", sa.BOOLEAN(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###
