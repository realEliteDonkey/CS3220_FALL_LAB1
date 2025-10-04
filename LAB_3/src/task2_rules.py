from src.locations import loc_A, loc_B

feeding_rules = {
    (((0,0), 'Empty'),): 'MoveRight', 
    (((1,0), 'Empty'),): 'MoveLeft', 
    
    (((0,0), 'MilkHere'),): 'Drink', 
    (((0,0), 'SausageHere'),): 'Eat', 
    
    (((1,0), 'MilkHere'),): 'Drink', 
    (((1,0), 'SausageHere'),): 'Eat',
    
    (((0,0), 'MilkHere'), ((0,0), 'Empty')): 'MoveRight',
    (((1,0), 'MilkHere'), ((1,0), 'Empty')): 'MoveLeft',
    
    (((0,0), 'SausageHere'), ((0,0), 'Empty')): 'MoveRight',
    (((1,0), 'SausageHere'), ((1,0), 'Empty')): 'MoveLeft',
    
    (((0,0), 'Empty'), ((1,0), 'SausageHere'), ((1,0), 'Empty')): 'MoveLeft',
    (((1,0), 'Empty'), ((0,0), 'SausageHere'), ((0,0), 'Empty')): 'MoveRight',
    
    (((0,0), 'Empty'), ((1,0), 'MilkHere'), ((1,0), 'Empty')): 'MoveLeft',
    (((1,0), 'Empty'), ((0,0), 'MilkHere'), ((0,0), 'Empty')): 'MoveRight'
}