from .exceptions import *
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.expression import select, insert, delete, update
from sqlalchemy.ext.asyncio.session import AsyncSession
from typing import Any, Optional, Dict


def and_exp(*args):
    return and_(*args)


def or_exp(*args):
    return or_(*args)


class MysqlUpdate:
    query = None

    def __init__(self, session: AsyncSession, table: Any, values, where_clause=None):
        self.session = session
        self.table = table
        self.query = update(table).values(values)
        self._where(where_clause)

    def _where(self, where_clause):
        try:
            self.query = self.query.where(where_clause)
        except BaseException:
            raise WhereQueryError

    async def execute(self):
        try:
            result = await self.session.execute(self.query)
            return result
        except BaseException:
            raise UpdateExecutionError


class MysqlInsert:
    query = None

    def __init__(self, session: AsyncSession, table: Any, values):
        self.session = session
        self.table = table
        self.query = insert(table).values(values)

    async def execute(self):
        try:
            result = await self.session.execute(self.query)
            return result
        except BaseException:
            raise InsertExecutionError


class MysqlDelete:
    query = None

    def __init__(self, session: AsyncSession, table: Any, where_clause=None):
        self.session = session
        self.table = table
        self.query = delete(table)
        self._where(where_clause)

    def _where(self, where_clause):
        try:
            self.query = self.query.where(where_clause)
        except BaseException:
            raise WhereQueryError

    async def execute(self, execution_option: dict | None = None):
        try:
            if execution_option is None:
                result = await self.session.execute(self.query)
            else:
                result = await self.session.execute(self.query, execution_options=execution_option)
            return result
        except BaseException:
            raise DeleteExecutionError


class MysqlSelect:
    query = None

    def __init__(
            self,
            session: AsyncSession,
            table: Any,
            fetch: str = 'fetchall',
            limit=None,
            where_clause=None,
            with_for_update=False,
            join_table=None,
            join_clause=None,
            group_by=None,  # 추가: 그룹화
            having=None,  # 추가: HAVING
            order_by=None,  # 추가: ORDER BY
            **kwargs
    ):
        self.session = session
        self.table = table
        self.query = select(table)
        self.fetch = fetch
        self._limit(limit)
        self._where(where_clause=where_clause)
        self._join(target=join_table, on_clause=join_clause, **kwargs)
        self._group_by(group_by)  # 추가: 그룹화
        self._having(having)  # 추가: HAVING
        self._order_by(order_by)  # 추가: ORDER BY
        if with_for_update:
            self.query = self.query.with_for_update()

    async def execute(self):
        try:
            result = await self.session.execute(self.query)
            data = getattr(self, f'_{self.fetch}')(result)
            return data
        except BaseException:
            raise SelectExecutionError

    @staticmethod
    def _fetchall(result):
        result = getattr(result, 'fetchall')()
        return [d[0] for d in result]

    @staticmethod
    def _fetchone(result):
        return getattr(result, 'fetchone')()[0]

    def _where(self, where_clause):
        if where_clause is not None:
            try:
                self.query = self.query.where(where_clause)
            except BaseException:
                raise WhereQueryError

    def _join(self, target, on_clause, **kwargs):
        """ not supported yet """
        pass

    def _limit(self, limit):
        if limit is not None:
            try:
                self.query = self.query.limit(limit)
            except BaseException:
                raise LimitQueryError

    def _group_by(self, group_by):
        if group_by is not None:
            try:
                self.query = self.query.group_by(group_by)
            except BaseException:
                raise GroupByQueryError

    def _having(self, having):
        if having is not None:
            try:
                self.query = self.query.having(having)
            except BaseException:
                raise HavingQueryError

    def _order_by(self, order_by):
        if order_by is not None:
            try:
                self.query = self.query.order_by(order_by)
            except BaseException:
                raise OrderByQueryError


class MysqlManager:
    dml_s = ('select', 'insert', 'delete', 'update')

    def __init__(self, session: AsyncSession, table: Optional = None):
        self.session = session
        self.table = table

    async def select(
            self,
            table: Any = None,
            columns: Optional[list] = None,
            limit: Optional[int] = None,
            fetch: Optional[str] = 'fetchall',
            where_clause=None,
            **kwargs
    ):
        """
            :param table: 사전 정의된 테이블 schema
            :param columns: select 하고 싶은 컬럼
            :param limit: int 형의 select 갯수
            :param fetch: fetch 타입 (fetchall, fetchone)
            :param where_clause: where 절의 bool 타입 조건들 (and, or 사용 가능)
            :param kwargs: select 쿼리에서 사용 가능한 옵션들
                        (with_for_update, join, order_by, having, group_by...)
        """
        if table is None:
            if columns is None:
                table = self.table
            else:
                table = columns

        try:
            query = MysqlSelect(self.session, table, fetch, limit, where_clause, **kwargs)
            result = await query.execute()
            return result
        except DatabaseQueryError:
            raise DatabaseQueryError

    async def delete(
            self,
            table: Any = None,
            where_clause=None,
            execution_option=None
    ):
        """
        :param execution_option: 실행시 옵션
        :param table: 삭제할 테이블 schema
        :param where_clause: 삭제할 데이터를 결정하는 조건
        """

        if table is None:
            table = self.table

        try:
            query = MysqlDelete(self.session, table, where_clause)
            await query.execute(execution_option)
        except DatabaseQueryError:
            raise DatabaseQueryError

    async def insert(
            self,
            table: Any = None,
            values: Dict[str, Any] | list | None = None,
    ):
        """
        :param table: 삽입할 테이블 schema
        :param values: 삽입할 데이터 값
        """
        if table is None:
            table = self.table

        try:
            query = MysqlInsert(self.session, table, values)
            await query.execute()
        except DatabaseQueryError:
            raise DatabaseQueryError

    async def update(
            self,
            table: Any,
            values: Dict[str, Any],
            where_clause=None,
    ):
        """
        :param table: 업데이트할 테이블 schema
        :param values: 업데이트할 데이터 값
        :param where_clause: 업데이트 대상을 결정하는 조건
        """
        if table is None:
            table = self.table

        try:
            query = MysqlUpdate(self.session, table, values, where_clause)
            await query.execute()
        except DatabaseQueryError:
            raise DatabaseQueryError

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def close(self):
        await self.session.close()
