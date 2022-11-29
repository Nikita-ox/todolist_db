#

# Категории
from django.db.models import Q
from rest_framework import permissions, filters
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination

from goals.models import GoalCategory, Goal
from goals.serializers import GoalCategoryCreateSerializer, GoalCategorySerializer, GoalCreateSerializer, GoalSerializer


class GoalCategoryCreateView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    # filterset_fields = ["board"]

    def get_queryset(self):
        return GoalCategory.objects.filter(user=self.request.user, is_deleted=False)


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GoalCategory.objects.filter(user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: GoalCategory):
        instance.is_deleted = True
        instance.save(update_fields=('is_deleted',))
        return instance


# Цели
class GoalCreateView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCreateSerializer


class GoalListView(ListAPIView):
    model = Goal
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ["due_date"]
    ordering = ["-priority", "due_date"]
    search_fields = ["title", "description"]

    def get_queryset(self):
        return Goal.objects.filter(
            Q(user_id=self.request.user.id) & ~Q(status=Goal.Status.archived)

        )


class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(
            Q(user_id=self.request.user.id) & ~Q(status=Goal.Status.archived)

        )



#
# # Комментарии
# class CommentCreateView(CreateAPIView):
# 	model = GoalComment
# 	permission_classes = [permissions.IsAuthenticated, CommentPermissions]
# 	serializer_class = serializers.CommentCreateSerializer
#
#
# class CommentListView(ListAPIView):
# 	model = GoalComment
# 	serializer_class = serializers.CommentSerializer
# 	pagination_class = LimitOffsetPagination
# 	permission_classes = [permissions.IsAuthenticated, CommentPermissions]
# 	ordering = ["-created"]
# 	filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
# 	filterset_fields = ["goal"]
#
# 	def get_queryset(self) -> GoalComment:
# 		return GoalComment.objects.filter(goal__category__board__participants__user=self.request.user)
#
#
# class CommentView(RetrieveUpdateDestroyAPIView):
# 	model = GoalComment
# 	serializer_class = serializers.CommentSerializer
# 	permission_classes = [permissions.IsAuthenticated, CommentPermissions]
#
# 	def get_queryset(self) -> GoalComment:
# 		return GoalComment.objects.filter(goal__category__board__participants__user=self.request.user)
#
#
# # Доски
# class BoardCreateView(CreateAPIView):
# 	model = Board
# 	permission_classes = [permissions.IsAuthenticated]
# 	serializer_class = serializers.BoardCreateSerializer
#
#
# class BoardListView(ListAPIView):
# 	model = Board
# 	serializer_class = serializers.BoardListSerializer
# 	pagination_class = LimitOffsetPagination
# 	permission_classes = [permissions.IsAuthenticated]
# 	ordering = ["title"]
# 	filter_backends = [filters.OrderingFilter]
#
# 	def get_queryset(self) -> Board:
# 		return Board.objects.filter(participants__user=self.request.user, is_deleted=False)
#
#
# class BoardView(RetrieveUpdateDestroyAPIView):
# 	model = Board
# 	permission_classes = [permissions.IsAuthenticated, BoardPermissions]
# 	serializer_class = serializers.BoardSerializer
#
# 	def get_queryset(self) -> Board:
# 		return Board.objects.filter(participants__user=self.request.user, is_deleted=False)
#
# 	def perform_destroy(self, instance: Board) -> Board:
# 		with transaction.atomic():
# 			instance.is_deleted = True
# 			instance.save()
# 			instance.categories.update(is_deleted=True)
# 			Goal.objects.filter(category__board=instance).update(
# 				status=Goal.Status.archived
# 			)
# 		return instance
