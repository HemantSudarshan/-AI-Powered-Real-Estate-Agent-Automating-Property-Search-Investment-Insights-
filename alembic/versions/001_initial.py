"""Initial migration - create all tables

Revision ID: 001_initial
Revises: 
Create Date: 2026-01-12

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create properties table
    op.create_table(
        'properties',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('price', sa.Float(), nullable=True),
        sa.Column('location', sa.String(length=255), nullable=True),
        sa.Column('property_type', sa.String(length=50), nullable=True),
        sa.Column('bedrooms', sa.Integer(), nullable=True),
        sa.Column('bathrooms', sa.Integer(), nullable=True),
        sa.Column('area_sqft', sa.Float(), nullable=True),
        sa.Column('amenities', sa.Text(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('source_url', sa.String(length=1000), nullable=True),
        sa.Column('city', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_properties_city', 'properties', ['city'], unique=False)
    op.create_index('ix_properties_property_type', 'properties', ['property_type'], unique=False)

    # Create search_history table
    op.create_table(
        'search_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('city', sa.String(length=100), nullable=False),
        sa.Column('property_type', sa.String(length=50), nullable=True),
        sa.Column('max_price', sa.Float(), nullable=True),
        sa.Column('results_count', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_search_history_created_at', 'search_history', ['created_at'], unique=False)

    # Create investment_analyses table
    op.create_table(
        'investment_analyses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('property_id', sa.Integer(), nullable=False),
        sa.Column('roi_5yr', sa.Float(), nullable=True),
        sa.Column('roi_10yr', sa.Float(), nullable=True),
        sa.Column('appreciation_rate', sa.Float(), nullable=True),
        sa.Column('rental_yield', sa.Float(), nullable=True),
        sa.Column('risk_score', sa.Integer(), nullable=True),
        sa.Column('recommendation', sa.String(length=50), nullable=True),
        sa.Column('analysis_details', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['property_id'], ['properties.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('investment_analyses')
    op.drop_index('ix_search_history_created_at', table_name='search_history')
    op.drop_table('search_history')
    op.drop_index('ix_properties_property_type', table_name='properties')
    op.drop_index('ix_properties_city', table_name='properties')
    op.drop_table('properties')
