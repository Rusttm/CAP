sql requests examples

1. select customers (meta) in actual groups for balance:
"""SELECT t.meta FROM public.customers_model t WHERE t.tags && ARRAY(SELECT tag FROM public.actual_customer_groups_model);"""
