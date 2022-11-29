#

# Категории
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, filters
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination

from goals.models import GoalCategory, Goal, GoalComment
from goals.serializers import GoalCategoryCreateSerializer, GoalCategorySerializer, GoalCreateSerializer, \
    GoalSerializer, GoalCommentCreateSerializer, GoalCommentSerializer


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
        # Вот тут поправить, как доктор прописал.
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


class CommentCreateView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentCreateSerializer


class CommentListView(ListAPIView):
    model = GoalComment
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination
    serializer_class = GoalCommentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filter_fields = ['goal']
    ordering = ["-created"]

    def get_queryset(self):
        return GoalComment.objects.filter(user_id=self.request.user.id)


class GoalCommentView(RetrieveUpdateDestroyAPIView):
    model = GoalComment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentSerializer

    def get_queryset(self):
        return GoalComment.objects.filter(user_id=self.request.user.id)
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
