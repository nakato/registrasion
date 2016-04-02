import itertools

from django.db.models import Q
from django.db.models import Sum
from registrasion import models as rego

from category import CategoryController
from conditions import ConditionController


class ProductController(object):

    def __init__(self, product):
        self.product = product

    @classmethod
    def available_products(cls, user, category=None, products=None):
        ''' Returns a list of all of the products that are available per
        enabling conditions from the given categories.
        TODO: refactor so that all conditions are tested here and
        can_add_with_enabling_conditions calls this method. '''
        if category is None and products is None:
            raise ValueError("You must provide products or a category")

        if category is not None:
            all_products = rego.Product.objects.filter(category=category)
        else:
            all_products = []

        if products is not None:
            all_products = itertools.chain(all_products, products)

        out = [
            product
            for product in all_products
            if CategoryController(product.category).user_quantity_remaining(user) > 0
            if cls(product).user_quantity_remaining(user) > 0
            if cls(product).can_add_with_enabling_conditions(user, 0)
        ]
        out.sort(key=lambda product: product.order)
        return out

    def user_quantity_remaining(self, user):
        ''' Returns the quantity of this product that the user add in the
        current cart. '''

        prod_limit = self.product.limit_per_user

        if prod_limit is None:
            # Don't need to run the remaining queries
            return 999999  # We can do better

        carts = rego.Cart.objects.filter(
            user=user,
            active=False,
            released=False,
        )

        items = rego.ProductItem.objects.filter(
            cart__in=carts,
            product=self.product,
        )

        prod_count = items.aggregate(Sum("quantity"))["quantity__sum"] or 0

        return prod_limit - prod_count

    def can_add_with_enabling_conditions(self, user, quantity):
        ''' Returns true if the user is able to add _quantity_ to their count
        of this Product without exceeding the ceilings the product is attached
        to. '''

        conditions = rego.EnablingConditionBase.objects.filter(
            Q(products=self.product) | Q(categories=self.product.category)
        ).select_subclasses()

        mandatory_violated = False
        non_mandatory_met = False

        for condition in conditions:
            cond = ConditionController.for_condition(condition)
            met = cond.is_met(user, quantity)

            if condition.mandatory and not met:
                mandatory_violated = True
                break
            if met:
                non_mandatory_met = True

        if mandatory_violated:
            # All mandatory conditions must be met
            return False

        if len(conditions) > 0 and not non_mandatory_met:
            # If there's any non-mandatory conditions, one must be met
            return False

        return True
