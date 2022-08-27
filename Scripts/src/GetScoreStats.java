import java.io.*;

public class GetScoreStats {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new FileReader(args[0]));
        PrintWriter pw = new PrintWriter(new PrintWriter(new FileWriter("score_out.txt")));
        String line;
        double count = 0;
        double sum = 0;
        while ((line = br.readLine()) != null) {
            count++;
            double score = Double.parseDouble(line.split("\t")[1]);
            sum += score;
            if (count == 1 || count == 25) {
                double out = sum/count;
                pw.println(out);
            }
        }
        double out = sum/count;
        pw.println(out);
        pw.close();
        br.close();
    }
}
