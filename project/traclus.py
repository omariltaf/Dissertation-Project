from trajectory_partitioning import trajectory_partitioning

def traclus(trajectories):

    ######################################################## PARTITIONING PHASE
    all_line_segments = set()
    for trajectory in trajectories:
        # TODO: Execute Approximate Trajectory Partitioning
        # The result will be a set of line segments
        # trajectory.display()
        # if trajectory.length() == 4:
            trajectory_line_segments = trajectory_partitioning(trajectory)
            all_line_segments.update(trajectory_line_segments)
            # break
        # TODO: SORTING RESULTS?
        # break
    print(len(all_line_segments))
    for segment in all_line_segments:
        print(segment.timestamp)

    ############################################################ GROUPING PHASE
    # TODO: Line Segment Clusering
    # The result will be a set of clusters

    # for cluster in clusters:
        # TODO: Execute Representative Trajectory Generation
        # The result will be a representative trajectory for each cluster
