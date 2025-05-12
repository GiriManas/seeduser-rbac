    # Join after filtering both tables
    db_result = (
        db.query(TopicLensx, TopicLensxSession)
        .join(TopicLensxSession, TopicLensx.id == TopicLensxSession.topic_id)
        .filter(
            TopicLensx.id == sessionId,
            TopicLensx.user_id == user.user_id,
            TopicLensx.deprecated == False,
            TopicLensxSession.topic_id == sessionId,
            TopicLensxSession.deprecated == False
        )
        .first()
    )

    if not db_result:
        raise HTTPException(
            status_code=400,
            detail="Topic id {} not found or configuration missing".format(sessionId)
        )

    topic, topic_session = db_result

    if not topic_session.scatterplot_distribution:
        raise HTTPException(
            status_code=400,
            detail="Topic id {} has no cluster results".format(sessionId)
        )

    return topic_session.scatterplot_distribution