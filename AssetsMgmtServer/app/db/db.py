import time
import os
from threading import RLock

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy import Sequence
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

Base = declarative_base()

class User(Base):
    """DB User Table/Object definition
    """
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String, default="DefaultUser", unique=True)
    full_name = Column(String, default="Default User")
    email = Column(String, default="user@demo.com")
    password = Column(String, default="00000000")
    add_time = Column(Float, default=0.0)
    status = Column(String, default="active")

    # def __init__(self, name, full_name, email, password):
    #     self.name = name
    #     self.full_name = full_name
    #     self.email = email
    #     self.password = password
    #
    # def __repr__(self):
    #     return "<User('%s','%s', '%s', '%s')>" % (self.name, self.full_name, self.email, self.password)


# class ont(Base):
#     """DB ont Table/Object definition
#     """
#     __tablename__ = "ont"
#
#     id = Column(Integer, primary_key=True)
#     premises_label = Column(String, default="CDC-PRE-0001", unique=True)
#     board_type = Column(String, default="844G-1")
#     fsan = Column(String, default="CXNK00000000")
#     serial_number = Column(String, default="260406100000")
#     mac_address = Column(String, default="000000000000")
#     owner = Column(String, ForeignKey('user.id'))
#     add_time = Column(Float, default=0.0)
#     status = Column(String, default="active")


class _AssetsMgmtDB(object):
    """Assets Management result/log database class. It is designed to be thread-safe.
    """

    state = "disconnect"

    # lock = RLock()
    def __init__(self, db_uri="sqlite:///my_sqlite.db", echo=True, logger=None):
        """constructor

        Args:
            db_uri (string): data url string. default ("sqlite:///my_sqlite.db")
            echo (bool): True - to turn on the sqlachemy debug log print; False otherwise
            logger (object): Cafe CLogger object

        Returns:
            None

        """
        self.state = "disconnect"
        self.db_uri = db_uri
        # if logger is None:
        #     self.logger = Logger("assetsMgmtdb")
        # else:
        #     self.logger = logger
        try:
            engine = self.db_engine = create_engine(db_uri,
                                                    echo=echo)
            Base.metadata.create_all(engine)
            session_factory = sessionmaker(bind=engine)
            # self.Session = session_factory
            self.Session = scoped_session(session_factory)
            print "__init__ Here 3"
        except:
            # self.logger.error(msg=" - db_uri=%s" % str(db_uri),
            #              signal=DB_CONNECT_FAILED)
            return
        self.state = "connected"
        print "__init__ Here 4"
        # self.logger.debug("db (%s) create success" % str(db_uri))

    @staticmethod
    def return_db_uri(db_type, abs_db_path):
        """static method to return a sqlalchemy uri with timestamp

        Args:
            db_type: (string) - database type. eg sqlite.
            abs_db_path: absolute pathname of the database file or uri

        Returns:
            string - db uri

        """
        t = time.localtime()
        t1 = time.strftime("%Y%m%d", t)
        t2 = time.strftime("%Y%m%d%H%M%S", t)
        s =  "sqlite:///%s/%s/%s.idb" % (abs_db_path, t1, t2 )
        #note:
        # problem to run in memory database with multithread
        # should consider linux RAM disk solution
        #s = "sqlite:///:memory:"
        return s

    @staticmethod
    def get_db_uri_from_file(db_type, db_file):
        """static method to return a sqlalchemy uri form a file

        Args:
            db_type (string): database type. eg sqlite.
            abs_db_path: absolute pathname of the database file or uri

        Returns:
            string: db uri

        """
        s =  "sqlite:///%s" % (db_file)
        return s

    @staticmethod
    def get_path_from_uri(uri):
        """static method to return db file pathname from uri

        Args:
            uri (string): string of sqlachemy db uri

        Returns:
            string: db file pathname

        """
        return uri.split("///")[1]

    @staticmethod
    def create_path_from_uri(uri):
        """static method to to create file folder path uri

        Args:
            uri (string): string of sqlachemy db uri

        Returns:
            None

        """
        p = AssetsMgmtDB.get_path_from_uri(uri)
        try:
            os.makedirs(os.path.dirname(p))
        except:
            pass
        return os.path.isdir(os.path.dirname(p))

    def get_db_uri(self):
        """static method to return db uri

        Returns:
            string: db uri

        """
        return self.db_uri

    def _create_user(self, name, full_name, email, password, add_time):
        """internal method. create user in idb.
        #
        # Args:
        #     name (string): name of testsuite (unique identifier of test suite). if "name" is already exists, the existing
        #         ts_id corresponding to "name" will be returned.
        #     start_time (float): epoch seconds when the test suite is created.
        #
        # Returns:
        #     ts_id (integer): test suite idb index

        """
        print "Create user Enter"
        if self.state is "disconnect":
            return -1
        # check and see if test suite already exist gracefully
        id = self.get_user_id(name)
        print "id=",id
        if id > -1:
            return id

        us = User(name=name, full_name=full_name, email=email, password=password, add_time=add_time)

        print us

        db_session = self.Session()
        db_session.add(us)
        # self.lock.acquire()
        print "_Create_User here 1"
        db_session.close()
        self.Session.commit()

        print "_Create_User here 2"
        # self.lock.release()
        id = -1
        q = db_session.query(User).filter(User.name == name)
        for us in q:
            id = us.id
            print us.name
        # db_session.close()
        self.Session.remove()
        # self.Session.close()
        return id

    def get_user_id(self, name):
        """idb api - get user id from name
        #
        # Args:
        #     name (string): name of test suite
        #
        # Returns:
        #     integer: test suite id

        """
        if self.state is "disconnect":
            return -1

        us = self.get_user(name)
        if us is None:
            return -1
        else:
            return us.id

    def get_user(self, name):
        """idb api - get test suite object from name

        Args:
            name (string): name of test suite

        Returns:
            test suite object

        """
        if self.state is "disconnect":
            return None
        print "find user here 0"
        q = None
        db_session = self.Session()
        try:
            q = db_session.query(User).\
                filter(User.name == name).first()
        except:
            pass
        finally:
            # db_session.close()
            self.Session.remove()
        return q

    # def create_testcase(self, group="", name="default", global_id= "000001", assignee="default", ts_id=-1,
    #                     start_time=0.0):
    #     tc_id = -1
    #     if start_time == 0.0:
    #         start_time = time.time()
    #     with self.lock:
    #         tc_id =  self._create_testcase(group, name, global_id, assignee, ts_id, start_time)
    #     if tc_id == -1:
    #         self.logger.error(msg=" - name (%s)" % name, signal=DB_TESTCASE_CREATE_FAILED)
    #     else:
    #         self.logger.debug("test case create success - name (%s) global_id (%s)" % (name, global_id))
    #
    #     self.current_testcase_id = tc_id
    #     return tc_id
    #
    #
    # def _create_testcase(self, group="", name="default_testcase", global_id= "000001", assignee="default", ts_id=-1,
    #                      start_time=time.time()):
    #     if self.state is "disconnect":
    #         return -1
    #
    #     tc_id = self.get_testcase_id(name, global_id, ts_id)
    #
    #     # create test case if it is not exist
    #     db_session = self.Session()
    #     if tc_id < 0:
    #         tc = TestCase(group=group, name=name, global_id=global_id, assignee=assignee, ts_id=ts_id,
    #                       start_time=start_time)
    #
    #         db_session.add(tc)
    #         self.Session.commit()
    #         tc = None
    #
    #     # get the test case id from the db.
    #     id = -1
    #     for tc in db_session.query(TestCase).filter(TestCase.name == name).\
    #             filter(TestCase.ts_id == ts_id ):
    #         id = tc.id
    #
    #     self.Session.remove()
    #     return id
    #
    # def get_testcase_id(self, name, global_id, ts_id):
    #     if self.state is "disconnect":
    #         return -1
    #     tc = self.get_testcase(name, global_id, ts_id)
    #     if tc is None:
    #         return -1
    #     else:
    #         return tc.id
    #
    # def get_testcase(self, name, global_id, ts_id):
    #     if self.state is "disconnect":
    #         return None
    #     q = None
    #     try:
    #         q = self.Session().query(TestCase).filter(TestCase.name == name).\
    #             filter(TestCase.ts_id == ts_id).filter(TestCase.global_id == global_id).first()
    #     except:
    #         pass
    #     finally:
    #         self.Session.remove()
    #     return q
    #
    # def get_testcase_by_global_id(self, global_id, ts_id):
    #     if self.state is "disconnect":
    #         return None
    #     q = None
    #     try:
    #         q = self.Session().query(TestCase).filter(TestCase.global_id == global_id).\
    #             filter(TestCase.ts_id).first()
    #     except:
    #         pass
    #     finally:
    #         self.Session.remove()
    #     return q
    #
    # # def get_testcase_by_id(self, tc_id):
    # #     if self.state is "disconnect":
    # #         return None
    # #     q = None
    # #     try:
    # #         q = self.Session().query(TestCase).filter(TestCase.id == tc_id).first()
    # #     except:
    # #         pass
    # #     finally:
    # #         self.Session.remove()
    # #     return q
    #
    # def update_testcase_elapsed_time(self, tc_id):
    #     db_session = self.Session()
    #     with self.lock:
    #         try:
    #             tc = self.Session().query(TestCase).filter(TestCase.id == tc_id).first()
    #             tc.elapsed_time = time.time() - tc.start_time
    #             self.Session.commit()
    #         except:
    #             warn("cannot update elasped_time for tc with id=%d" % tc_id)
    #     self.Session.remove()
    #
    # def create_teststep(self, ts_id=-1, tc_id=-1, title="", index="", sid="",
    #                     action="", target="", cmd="", response="",
    #                     status="indeterminate", test="unknown",
    #                     msg="", filename="",
    #                     line=-1, start_time=0.0, elapsed_time=0.0):
    #
    #     tstep_id = -1
    #     if start_time == 0.0:
    #         start_time = time.time()
    #
    #     with self.lock:
    #         tstep = self._create_teststep(ts_id=ts_id, tc_id=tc_id,
    #                         title=title, index=index, sid=sid,
    #                         action=action, target=target, cmd=cmd,
    #                         response=response, status=status, test=test,
    #                         msg=msg, filename=filename, line=line,
    #                         start_time=start_time, elapsed_time=elapsed_time)
    #     if tstep == -1:
    #         self.logger.error(msg=" - test step (ts_id=%d, tc_id=%d, index=%s, title=%s)" % (ts_id, tc_id, index, title),
    #                      signal=DB_TESTSTEP_CREATE_FAILED)
    #     else:
    #         #self.logger.debug(msg="test step create success - (ts_id=%d, tc_id=%d, index=%s, title=%s)" %
    #         #                 (ts_id, tc_id, index, title))
    #         if status == FAIL:
    #             m = "%s - %s:%s - %s:%s:%s" % ("**FAIL", title, msg, test, filename, line)
    #         elif status == PASS:
    #             m = "%s - %s:%s - %s:%s:%s" % ("*pass", title, msg, test, filename, line)
    #         else:
    #             m = "%s - %s:%s - %s:%s:%s" % (status, title, msg, test, filename, line)
    #         self.logger.debug(m)
    #         pass
    #     return tstep
    #
    # def _create_teststep(self, ts_id=-1, tc_id=-1, title="", index="", sid="",
    #                     action="", target="", cmd="", response="",
    #                     status="indeterminate", test="unknown",
    #                     msg="", filename="",
    #                     line=-1, start_time=time.time(), elapsed_time=0.0):
    #
    #     if self.state is "disconnect":
    #         return -1
    #
    #     step = TestStep(ts_id=ts_id, tc_id=tc_id, title=title, index=index, sid=sid,
    #                     action=action, target=target, cmd=cmd,
    #                     response=response, status=status,
    #                     test=test, msg=msg, filename=filename,
    #                     line=line, start_time=start_time,
    #                     elapsed_time=elapsed_time)
    #
    #     self.Session().add(step)
    #     self.Session.commit()
    #
    #     self.current_teststep_id = step.id
    #
    #     self.Session.remove()
    #     return step
    #
    # def update_testsuite_result(self, name):
    #     ts_id = self.get_testsuite_id(name)
    #
    #     if ts_id == -1:
    #         self.logger.error(" - name (%s) " % name, signal=DB_TESTSUITE_GET_ID_FAILED)
    #         return
    #     else:
    #         self.logger.debug("update test suite result (%s, %d)" % (name, ts_id))
    #
    #     self._update_testsuite_result(ts_id)
    #
    # def update_testsuite_result_current(self):
    #     self._update_testsuite_result(self.current_testsuite_id)
    #
    # def update_testsuite_result_by_id(self, ts_id):
    #     self._update_testsuite_result(ts_id)
    #
    # def _update_testsuite_result(self, ts_id):
    #
    #     # ts_id = self.get_testsuite_id(name)
    #     #
    #     # if ts_id == -1:
    #     #     self.logger.error(" - name (%s) " % name, signal=DB_TESTSUITE_GET_ID_FAILED)
    #     #     return
    #     # else:
    #     #     self.logger.debug("update test suite result (%s, %d)" % (name, ts_id))
    #
    #     #logger.debug("query for test cases in test suite (%s)" % name)
    #     db_session = self.Session()
    #     with self.lock:
    #
    #         #get testsuite object by name
    #         testsuite = db_session.query(TestSuite).\
    #             filter(TestSuite.id == ts_id).first()
    #
    #         #resetting testsuite information
    #         testsuite.tc_cnt = 0
    #         testsuite.tc_pass_cnt = 0
    #         testsuite.tc_fail_cnt = 0
    #         testsuite.tc_indeterminate_cnt = 0
    #         testsuite.status = INDETERMINATE
    #         testsuite.elapsed_time = 0.0
    #         self.Session.commit()
    #
    #         ts_pass = 0
    #         ts_fail = 0
    #         ts_indeterminate = 0
    #
    #
    #         #query test cases in test suite and loop thru all the stats
    #
    #         testcases = db_session.query(TestCase).filter(TestCase.ts_id == ts_id)
    #         tc_cnt = db_session.query(TestCase).filter(TestCase.ts_id == ts_id).count()
    #
    #         self.logger.debug("test suite (%d) has %d test cases" % (ts_id, tc_cnt))
    #
    #         for tc in testcases:
    #             # testcase stats
    #             _pass = db_session.query(TestStep).filter(TestStep.ts_id == ts_id,
    #                                                       TestStep.tc_id == tc.id,
    #                                                       TestStep.status == PASS).count()
    #             _fail = db_session.query(TestStep).filter(TestStep.ts_id == ts_id,
    #                                                           TestStep.tc_id == tc.id,
    #                                                           TestStep.status == FAIL).count()
    #             _info = db_session.query(TestStep).filter(TestStep.ts_id == ts_id,
    #                                                           TestStep.tc_id == tc.id,
    #                                                           TestStep.status == INFO).count()
    #             _warn = db_session.query(TestStep).filter(TestStep.ts_id == ts_id,
    #                                                           TestStep.tc_id == tc.id,
    #                                                           TestStep.status == WARN).count()
    #             _error = db_session.query(TestStep).filter(TestStep.ts_id == ts_id,
    #                                                           TestStep.tc_id == tc.id,
    #                                                           TestStep.status == ERROR).count()
    #
    #
    #             tc.id = tc.id
    #             tc.pass_cnt = _pass
    #             tc.fail_cnt = _fail
    #             tc.info_cnt = _info
    #             tc.warn_cnt = _warn
    #             tc.error_cnt = _error
    #
    #             tc.total_cnt = _pass + _fail + _info + _warn + _error
    #
    #             #tc.status = FAIL
    #             if tc.fail_cnt == 0 and tc.pass_cnt > 0:
    #                 tc.status = PASS
    #                 ts_pass += 1
    #             elif tc.fail_cnt == 0 and tc.pass_cnt == 0:
    #                 tc.status = INDETERMINATE
    #                 ts_indeterminate += 1
    #             else:
    #                 tc.status = FAIL
    #                 ts_fail += 1
    #
    #             self.Session.commit()
    #         #end of for loop
    #
    #         if tc_cnt != 0:
    #
    #             testsuite.tc_pass_cnt = ts_pass
    #             testsuite.tc_fail_cnt = ts_fail
    #             testsuite.tc_indeterminate_cnt = ts_indeterminate
    #             testsuite.tc_cnt = ts_pass + ts_fail + ts_indeterminate
    #             testsuite.elapsed_time = time.time() - testsuite.start_time
    #
    #             if ts_fail > 0:
    #                 testsuite.status = FAIL
    #             elif ts_pass > 0 and ts_fail == 0:
    #                 testsuite.status = PASS
    #             self.Session.commit()
    #
    #         self.Session.remove()
    #
    # def _get_summary_report_text(self):
    #     """
    #     get summary report of test execution
    #     :return: string of summary report
    #     """
    #     self.logger.debug("get summary report text")
    #     db_session = self.Session()
    #     testsuites = db_session.query(TestSuite.id, TestSuite.name,
    #                                   TestSuite.status, TestSuite.tc_cnt,
    #                                   TestSuite.tc_pass_cnt, TestSuite.tc_fail_cnt,
    #                                   TestSuite.tc_indeterminate_cnt,
    #                                   TestSuite.start_time, TestSuite.elapsed_time)
    #     self.Session.remove()
    #     x = PrettyTable(["id", "name", "status", "tc_num", "pass",
    #                      "fail", "indeterminate", "start_time", "elapsed_time"])
    #     x.align["id"] = "l"
    #     x.padding_width = 1 # One space between column edges and contents (default)
    #     for ts in testsuites:
    #         #print (ts)
    #         x.add_row(ts)
    #     ret = "*** summary report ***\n" + str(x)
    #     return ret
    #
    # def _get_testsuite_report_text(self, ts):
    #     """
    #     get test suite report
    #     :param ts: name or id of test suite
    #     :return: string of test suite report
    #     """
    #     if isinstance(ts, str):
    #         ts_id = self.get_testsuite_id(ts)
    #     elif isinstance(ts, int):
    #         ts_id = int(ts)
    #     else:
    #         ts_id = -1
    #
    #     if ts_id == -1:
    #         self.logger.error(msg=" - ts (%s)" % str(ts),
    #                      signal=DB_TESTSUITE_GET_ID_FAILED)
    #         return
    #     self.logger.debug("get testsuite report text (%s)" % str(ts))
    #     db_session = self.Session()
    #     testcases = db_session.query(TestCase.id, TestCase.ts_id,
    #                                  TestCase.group, TestCase.name, TestCase.global_id,
    #                                  TestCase.status, TestCase.assignee, TestCase.total_cnt,
    #                                  TestCase.pass_cnt, TestCase.fail_cnt,
    #                                  TestCase.info_cnt, TestCase.warn_cnt,
    #                                  TestCase.error_cnt, TestCase.start_time,
    #                                  TestCase.elapsed_time).filter(TestCase.ts_id == ts_id)
    #
    #     x = PrettyTable(["id", "ts_id", "group", "name", "global_id", "status", "assignee", "teststep_cnt", "pass",
    #                      "fail", "info", "warn", "error" , "start_time", "elapsed_time"])
    #     x.align["id"] = "l"
    #     x.padding_width = 1 # One space between column edges and contents (default)
    #     for tc in testcases:
    #         #print (tc)
    #         x.add_row(tc)
    #     self.Session.remove()
    #     ret = "*** test suite report (%s) ***\n" % str(ts) + str(x)
    #     return ret
    #
    # def _get_testcase_report_text(self, ts, tc_name, global_id):
    #     """
    #     get test case report
    #     :param global_id:
    #     :param ts: test suite name or id
    #     :param tc_name: test case name
    #     :return: string of test case report
    #     """
    #     if isinstance(ts, str):
    #         ts_id = self.get_testsuite_id(ts)
    #
    #     elif isinstance(ts, int):
    #         ts_id = int(ts)
    #     else:
    #         ts_id = -1
    #
    #     if ts_id == -1:
    #         logger.error(msg=" - ts (%s)" % str(ts),
    #                      signal=DB_TESTSUITE_GET_ID_FAILED)
    #         return
    #
    #     tc_id = self.get_testcase_id(tc_name, global_id, ts_id)
    #
    #     if tc_id == -1:
    #         logger.error(msg=" - tc (%s)" % name,
    #                      signal=DB_TESTCASE_GET_ID_FAILED)
    #         return
    #
    #     self.logger.debug("get testcase report text (%s %s)" % (ts, tc_name))
    #     db_session = self.Session()
    #     teststeps = db_session.query(TestStep.id, TestStep.ts_id, TestStep.tc_id,
    #                                  TestStep.status, TestStep.index, TestStep.sid,
    #                                  TestStep.title, TestStep.test, TestStep.msg,
    #                                  TestStep.action, TestStep.target, TestStep.cmd,
    #                                  TestStep.response, TestStep.filename,
    #                                  TestStep.line, TestStep.start_time,
    #                                  TestStep.elapsed_time).filter(TestStep.ts_id == ts_id,
    #                                                                TestStep.tc_id == tc_id)
    #
    #     self.Session.remove()
    #     x = PrettyTable(["id", "ts_id", "tc_id", "status", "index", "sid",
    #                      "title", "test", "msg", "action", "target",
    #                      "cmd", "response", "filename", "line", "start_time", "elapsed_time"])
    #     x.align["id"] = "l"
    #     x.padding_width = 1 # One space between column edges and contents (default)
    #     for s in teststeps:
    #         x.add_row(s)
    #     ret = "*** test case report (%s - %s) ***\n" % (ts, tc_name) + str(x)
    #     return ret
    #
    # def get_data(self, data_type=None):
    #     """Get Data in iDB DataTable.
    #
    #     Args:
    #         data_type (str): data_type of data. Default is None. if data_type is None. query all data.
    #     Returns:
    #         data (list of dict)
    #
    #     """
    #     db_session = self.Session()
    #     if data_type is None:
    #         d = db_session.query(DataTable)
    #     else:
    #         d = db_session.query(DataTable).filter(DataTable.data_type.like(data_type))
    #     self.Session.remove()
    #
    #     ret = []
    #     for _d in d:
    #         ret.append(_d.__dict__)
    #     return ret
    #
    # def _get_data_by_type_text(self, data_type=None):
    #     # db_session = self.Session()
    #     # if data_type is None:
    #     #     d = db_session.query(DataTable)
    #     # else:
    #     #     d = db_session.query(DataTable).filter_by(data_type=data_type)
    #     # self.Session.remove()
    #
    #     d = self.get_data(data_type)
    #
    #     #for s in d:
    #     #    print(s.__dict__)
    #
    #     #s = d[0].__dict__
    #     #x = PrettyTable(["id", "ts_id", "obj", "tc_id", "tstep_id",
    #     #                 "data_type", "data", "note", "filename",
    #     #                 "line", "timestamp"])
    #
    #     cnt = 0
    #     for s in d:
    #         if cnt == 0:
    #             x = PrettyTable(s.keys())
    #             #print(s.__dict__)
    #             #print(s.__dict__.keys())
    #             x.align["id"] = "l"
    #             x.padding_width = 1 # One space between column edges and contents (default)
    #             x.add_row(s.values())
    #         else:
    #             try:
    #                 x.add_row(s.values())
    #             except:
    #                 pass
    #         cnt += 1
    #     if cnt == 0:
    #         return ""
    #     else:
    #         return "*** test case report (%s) ***\n" % str(data_type) + str(x)
    #
    # def _get_testcase_report_by_id_text(self, tc_id):
    #     """
    #     get test case report
    #     :param tc_id: test case id
    #     :return: string of test case report
    #     """
    #     self.logger.debug("get testcase report text (%s)" %  tc_id)
    #     db_session = self.Session()
    #     teststeps = db_session.query(TestStep.id, TestStep.ts_id, TestStep.tc_id,
    #                                  TestStep.status, TestStep.index, TestStep.sid,
    #                                  TestStep.title, TestStep.test, TestStep.msg,
    #                                  TestStep.action, TestStep.target, TestStep.cmd,
    #                                  TestStep.response, TestStep.filename,
    #                                  TestStep.line, TestStep.start_time,
    #                                  TestStep.elapsed_time).filter(TestStep.tc_id == tc_id)
    #
    #     self.Session.remove()
    #     x = PrettyTable(["id", "ts_id", "tc_id", "status", "index", "sid",
    #                      "title", "test", "msg", "action", "target",
    #                      "cmd", "response", "filename", "line", "start_time", "elapsed_time"])
    #     x.align["id"] = "l"
    #     x.padding_width = 1 # One space between column edges and contents (default)
    #     for s in teststeps:
    #         x.add_row(s)
    #     ret = "*** test case report (%s) ***\n" % str(tc_id) + str(x)
    #     return ret
    #


AssetsMgmtDB = _AssetsMgmtDB