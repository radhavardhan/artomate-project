# import random
#
# class PrimaryRouter:
#     def db_for_read(self, model, **hints):
#
#         return random.choice(['a1', 'a2'])
#
#     def db_for_write(self, model, **hints):
#
#         return 'a1'
#
#     # def allow_relation(self, obj1, obj2, **hints):
#     #     """
#     #     Relations between objects are allowed if both objects are
#     #     in the primary/replica pool.
#     #     """
#     #     db_list = ('primary', 'replica1', 'replica2')
#     #     if obj1._state.db in db_list and obj2._state.db in db_list:
#     #         return True
#     #     return None
#
#     def allow_migrate(self, db, app_label, model_name=None, **hints):
#         """
#         All non-auth models end up in this pool.
#         """
#         return True
