import graphene
from graphene_django import DjangoObjectType

from bookshelf.models import Author, Book

class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "description")

class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        fields = ("id", "name", "surname")

class Query(graphene.ObjectType):
    all_authors= graphene.List(AuthorType)
    books_by_title = graphene.Field(BookType, title=graphene.String(required=True))
    books_per_author = graphene.List(BookType, author_name=graphene.String(required=False), author_surname=graphene.String(required=False))

    def resolve_all_authors(root, info):
        # We can easily optimize query count in the resolve method
        return Author.objects.all()

    def resolve_books_by_title(root, info, title):
        try:
            return Book.objects.select_related("author").get(title=title)
        except Book.DoesNotExist:
            return None

    def resolve_books_per_author(root, info, author_name=None, author_surname=None):
        query = Book.objects.select_related("author")
        if author_name:
            query = query.filter(author__name=author_name)
        if author_surname:
            query = query.filter(author__surname=author_surname)
        return query.all()


schema = graphene.Schema(query=Query)