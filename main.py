
def main():
    n = int(input().strip())
    teams = []

    for _ in range(n):
        team_id, domain, size = input().split()
        teams.append((team_id, domain, int(size)))

    m = int(input().strip())
    guides = []

    for i in range(m):
        guide_id, domain, capacity = input().split()
        guides.append({
            "id": guide_id,
            "domain": domain,
            "capacity": int(capacity),
            "remaining": int(capacity)
        })

    assignments = {}
    unassigned = []

    # Greedy allocation in input order
    for team_id, domain, size in teams:

        # Team size must be between 2 and 4
        if size < 2 or size > 4:
            unassigned.append(team_id)
            continue

        # Find a matching guide with maximum remaining capacity.
        # Ties are resolved by guide input order.
        best_guide = None

        for guide in guides:
            if (
                guide["domain"] == domain
                and guide["remaining"] >= 1
            ):
                if (
                    best_guide is None
                    or guide["remaining"] > best_guide["remaining"]
                ):
                    best_guide = guide

        if best_guide is not None:
            assignments[team_id] = best_guide["id"]
            best_guide["remaining"] -= 1
        else:
            unassigned.append(team_id)

    # Output assignments in team input order
    print("\n OUTPUT:\n")
    
    for team_id, _, _ in teams:
        if team_id in assignments:
            print(f"{team_id} {assignments[team_id]}")
        else:
            print(f"{team_id} UNASSIGNED")

    if unassigned:
        print("UNASSIGNED:", ", ".join(unassigned))
    else:
        print("UNASSIGNED: none")


if __name__ == "__main__":
    main()
