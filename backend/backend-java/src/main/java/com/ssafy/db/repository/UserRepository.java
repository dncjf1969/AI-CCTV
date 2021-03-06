package com.ssafy.db.repository;

import com.ssafy.db.entity.User;
import org.hibernate.sql.Insert;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

/**
 * 유저 모델 관련 디비 쿼리 생성을 위한 JPA Query Method 인터페이스 정의.
 */
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    // 아래와 같이, Query Method 인터페이스(반환값, 메소드명, 인자) 정의를 하면 자동으로 Query Method 구현됨.


    User saveAndFlush(User user);

    User findUserById(Long id);

    @Query("select u from User u where u.START_TIME < :curTime and u.END_TIME > :curTime")
    List<User> findByTime(@Param("curTime") LocalDateTime curTime);

    User findUserByEmail(String email);

    @Modifying(clearAutomatically = true)
    @Query("UPDATE User b SET b.START_TIME= :startTime, b.END_TIME= :endTime where b.email= :email")
    int setUserTimer(String email,LocalDateTime startTime, LocalDateTime endTime);

    // 정보를 들고오는게 아닌 유무만 확인
    boolean existsByEmail(String email);

    @Modifying(clearAutomatically = true)
    @Query("UPDATE User b SET b.password= :password where b.email= :email")
    int updatePassword(String email, String password);
}