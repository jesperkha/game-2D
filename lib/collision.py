# Version 1.0
# Collision functions

def collision_rect_rect(a: tuple, b: tuple) -> bool:
    """
        Checks to see if a collision is happening between two objects.
        `a` and `b` are tuples with x, y, w, h values in that order.
    """
    
    # Checks to see if the other object is too far from this collider to have a collision
    # If any of these statements are true then a collision is not possible because theres
    # no way the two objects are intersecting eachother.

    # Side relative to THIS collider
    top    = a[1] > b[1] + b[3]
    left   = a[0] > b[0] + b[2]
    right  = a[0] + a[2] < b[0]
    bottom = a[1] + a[3] < b[1]

    is_colliding = top or left or right or bottom
    # When true, a collision is not possible because the
    # rects are outside eachother.
    return not is_colliding


def find_collision_rect_rect(a: tuple, b: tuple) -> str:
    """
        Finds the side the collision is happening on relative to the object its called from.\n
        Params:\n
        \ta, b: Object with pos and size vector
        Returns:\n
        \tstr: Side where collision is happening (left, right, top, bottom)
    """

    # Function returns the side of the collision of two objects in relation to THIS collider.
    # Ex: Right side of this object touches left side of other, will return right
    
    # Delta x and y are difference in height between the two colliders.
    # If one is smaller than the other it means the collision is happening on that axis.
    dx = a.pos.x + a.size.x / 2 - (b.pos.x + b.size.x / 2)
    dy = a.pos.y + a.size.y / 2 - (b.pos.y + b.size.y / 2)

    # If the distance of delta x is greater than delta y it means that the collision is happening
    # on the x axis.
    if dx * dx > dy * dy:
        
        # If delta x is greater than 0, the collision is happening on the right side
        if dx > 0:
            return "right"

        # Otherwise its on the left side
        else:
            return "left"

    # If delta y is a longer distance, the collision is on the y axis
    else:

        # If delta y if greater than 0, the collision must be on the bottom
        if dy > 0:
            return "bottom"

        # Otherwise its on the top
        else:
            return "top"

    # Side note:
    # This method can be used without the need of a collison. It will just return the side the other
    # collider is on in relation to this one.