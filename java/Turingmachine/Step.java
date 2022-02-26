import java.util.Arrays;

public class Step {
    final int  write;
    final int move;
    final int zustand;

    public Step(int q , int w, int m){
        write = w;
        move = m;
        zustand = q;
    }
    public Step(int seed){
        write = seed % 3;
        seed = seed / 3;
        move = (seed % 3) - 1;
        seed = seed / 3;
        zustand = seed % 3;
    }
    public int getMove() {
        return move;
    }
    public int getWrite() {
        return write;
    }
    public int getZustand() {
        return zustand;
    }
    public String toString(){
        String direction = "";
        switch(move){
            case -1 : direction = "L";
            break;
            case 0 : direction = "N";
            break;
            case 1 : direction = "R";
            break;
            default: throw new IllegalStateException("move ist invalied");
        }
        return "(q" + zustand + ", " + write + ", "+ direction+")";
    }  
    

}
