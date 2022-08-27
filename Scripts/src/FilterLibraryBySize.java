import java.io.*;
import java.util.ArrayList;

public class FilterLibraryBySize {
    public static void main(String[] args) throws IOException, InterruptedException {
        if(args.length != 3 || args[0].equalsIgnoreCase("--help")){
            System.out.println( "Usage: Filter Binding Site Library" );
            System.out.println( "          -opts  [list path]" );
            System.out.println( "                 [min size]" );
            System.out.println( "                 [max size]" );
            return;
        }

        BufferedReader br = new BufferedReader(new FileReader(args[0]));
        PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter("new_list.txt")));
        int minSize = Integer.parseInt(args[1]);
        int maxSize = Integer.parseInt(args[2]);

        String lineIn;
        int count = 0;
        while ((lineIn = br.readLine()) != null) {
            int bsSize = Integer.parseInt(lineIn.split(" ")[1]);

            if (bsSize >= minSize && bsSize <= maxSize) {
                pw.println(lineIn.split(" ")[0]);
                count++;
            }
        }

        br.close();
        pw.close();
    }
}
