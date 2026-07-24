from sqlalchemy import BigInteger, String, DateTime, Integer, ForeignKey, Boolean, func, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id:         Mapped[int]  = mapped_column(primary_key=True)
    tg_id:      Mapped[int]  = mapped_column(BigInteger, unique=True, nullable=False)
    full_name:  Mapped[str]  = mapped_column(String, nullable=False)
    phone:      Mapped[str]  = mapped_column(String, nullable=True)
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    language:   Mapped[str]  = mapped_column(String, default="uz", nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    enrollments: Mapped[list["Enrollment"]] = relationship(back_populates="user")
    
    def __repr__(self):
        return f"<User tg_id={self.tg_id} name={self.full_name}>" 

    
class Course(Base):
    __tablename__ = "courses"

    id:          Mapped[int] = mapped_column(primary_key=True)
    title:       Mapped[str] = mapped_column(String, nullable=False)   
    description: Mapped[str] = mapped_column(Text, nullable=True)      
    is_active:   Mapped[bool] = mapped_column(Boolean, default=True)  
    created_at:  Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    lessons:     Mapped[list["Lesson"]] = relationship(back_populates="course")
    enrollments: Mapped[list["Enrollment"]] = relationship(back_populates="course")
    
    def __repr__(self):  
        return f"<Course id={self.id} title={self.title}>"  


class Lesson(Base):
    __tablename__ = "lessons"

    id:          Mapped[int] = mapped_column(primary_key=True)
    course_id:   Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)
    title:       Mapped[str] = mapped_column(String, nullable=False)   
    content:     Mapped[str] = mapped_column(Text, nullable=True)      
    video_url:   Mapped[str] = mapped_column(String, nullable=True)    
    order:       Mapped[int] = mapped_column(Integer, default=1)       
    course: Mapped["Course"] = relationship(back_populates="lessons")
    media:  Mapped[list["LessonMedia"]] = relationship(back_populates="lesson")    
    
    def __repr__(self):
        return f"<Lesson id={self.id} title={self.title}>" 


class LessonMedia(Base):
    __tablename__ = "lesson_media"

    id:         Mapped[int] = mapped_column(primary_key=True)
    lesson_id:  Mapped[int] = mapped_column(ForeignKey("lessons.id"), nullable=False)
    media_type: Mapped[str] = mapped_column(String, nullable=False)
    file_id:    Mapped[str] = mapped_column(String, nullable=False)
    caption:    Mapped[str] = mapped_column(String, nullable=True)

    lesson: Mapped["Lesson"] = relationship(back_populates="media")

    def __repr__(self):
        return f"<LessonMedia type={self.media_type} lesson={self.lesson_id}>"


class Enrollment(Base):
    __tablename__ = "enrollments"

    id:          Mapped[int] = mapped_column(primary_key=True)
    user_id:     Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    course_id:   Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)
    enrolled_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    user:   Mapped["User"]   = relationship(back_populates="enrollments")
    course: Mapped["Course"] = relationship(back_populates="enrollments")