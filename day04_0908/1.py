def print_gugudan_columns(start, end):
    """지정된 범위의 구구단을 가로(열) 방향으로 예쁘게 출력합니다."""
    print("=" * 80)
    # 단 제목 출력
    headers = [f"     [ {dan}단 ]     " for dan in range(start, end + 1)]
    print("".join(headers))
    print("=" * 80)
    
    # 1부터 9까지 곱셈 결과 출력
    for i in range(1, 10):
        row_items = []
        for dan in range(start, end + 1):
            # 정렬하여 열 맞춤
            expr = f"{dan} x {i} = {dan * i:2d}"
            row_items.append(f"   {expr:<14}")
        print("".join(row_items))
    print("=" * 80)
    print()


def print_all_gugudan_beautiful():
    """전체 구구단을 4개 단씩 나누어 가로로 출력합니다."""
    print("\n" + "*" * 33 + " [ 구구단 전체 출력 ] " + "*" * 33)
    # 2단 ~ 5단 출력
    print_gugudan_columns(2, 5)
    # 6단 ~ 9단 출력
    print_gugudan_columns(6, 9)


def print_all_gugudan_vertical():
    """전체 구구단을 2단부터 9단까지 세로로 길게 출력합니다."""
    print("\n" + "*" * 33 + " [ 구구단 세로 출력 ] " + "*" * 33)
    for dan in range(2, 10):
        print(f"\n--- [ {dan}단 ] ---")
        for i in range(1, 10):
            print(f"{dan} x {i} = {dan * i:2d}")
    print("=" * 80)
    print()


def print_specific_gugudan():
    """사용자가 입력한 특정 단의 구구단을 출력합니다."""
    while True:
        try:
            user_input = input("\n출력할 단을 입력하세요 (2 ~ 9) 또는 'q'를 입력하여 이전 메뉴로: ").strip()
            if user_input.lower() == 'q':
                break
            
            dan = int(user_input)
            if 2 <= dan <= 9:
                print("\n" + "=" * 30)
                print(f"      [ {dan}단 출력 ]")
                print("=" * 30)
                for i in range(1, 10):
                    print(f"   {dan} x {i} = {dan * i:2d}")
                print("=" * 30)
                break
            else:
                print("[경고] 2에서 9 사이의 숫자를 입력해주세요.")
        except ValueError:
            print("[에러] 올바른 숫자 또는 'q'를 입력해주세요.")


def main():
    while True:
        print("\n" + "★" * 15 + " 구구단 프로그램 " + "★" * 15)
        print(" 1. 전체 구구단 출력 (가로 정렬 - 추천)")
        print(" 2. 전체 구구단 출력 (세로 정렬)")
        print(" 3. 특정 단 출력")
        print(" 4. 프로그램 종료")
        print("★" * 40)
        
        choice = input("원하는 메뉴 번호를 선택하세요 (1~4): ").strip()
        
        if choice == '1':
            print_all_gugudan_beautiful()
        elif choice == '2':
            print_all_gugudan_vertical()
        elif choice == '3':
            print_specific_gugudan()
        elif choice == '4':
            print("\n구구단 프로그램을 종료합니다. 이용해 주셔서 감사합니다!")
            break
        else:
            print("[경고] 잘못된 입력입니다. 1, 2, 3, 4 중 하나를 선택해 주세요.")


if __name__ == "__main__":
    main()
