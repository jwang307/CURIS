import java.io.*;
import java.util.ArrayList;

/**
 * Filter out all binding sites that are less than 11 residues or greater than 34 residues in length/
 * arguments are the paths to the lib and cf lib directories and the file that contains all BS names.
 */

public class FilterLibrary {

    public static final int MIN_SIZE = 11;
    public static final int MAX_SIZE = 34;

    public static void main(String[] args) throws IOException, InterruptedException {
        if(args.length != 3 || args[0].equalsIgnoreCase("--help")){
            System.out.println( "Usage: Filter Binding Site Library" );
            System.out.println( "          -opts  [library dir path]" );
            System.out.println( "                 [cf library dir path]" );
            System.out.println( "                 [list of binding sites]" );
            return;
        }

        BufferedReader br = new BufferedReader(new FileReader(args[2]));
        String libPath = args[0];
        String cfPath = args[1];

        String lineIn;
        ArrayList<String> filteredBS = new ArrayList<>();
        int invalid = 0;
        while ((lineIn = br.readLine()) != null) {
            BufferedReader bsFile = new BufferedReader(new FileReader(libPath + lineIn));

            boolean toFilter = false;
            int numResidues = 0;

            String pdbIn;
            int prevId = 0, currId;
            while ((pdbIn = bsFile.readLine()) != null) {
                if (!pdbIn.startsWith("ATOM")) {
                    break;
                }
                // TODO: Only allows for max 100,000 atoms in pdb
                String residueNum = pdbIn.substring(24, 30).replaceAll("\\D+", "");

                currId = Integer.parseInt(residueNum.trim());

                if (numResidues > MAX_SIZE) {
                    toFilter = true;
                }

                if (numResidues > 100) {
                    break;
                }

                if (currId != prevId) {
                    numResidues++;
                    prevId = currId;
                }
            }

            if (numResidues < MIN_SIZE) {
                toFilter = true;
            }

            System.out.println(lineIn + " " + numResidues);
            if (toFilter) {
                invalid++;
                for (int i = 0; i < 3; i++) {
                    Runtime rt = Runtime.getRuntime();
                    Process pr;
                    String command;
                    command = "rm " + (i == 0? cfPath + lineIn.substring(0, lineIn.length() - 4) + "-cf.pdb" :
                            libPath + (i == 1? lineIn : lineIn.replaceAll("BS", "lig")));
                    pr = rt.exec(command);
                    pr.waitFor();
                    pr.destroy();
                }
                // delete ligand, bs, and cf
            } else {
                filteredBS.add(lineIn);
            }

            bsFile.close();
        }

        br.close();
        System.out.println(invalid);
        PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter("new_list.txt")));

        for (String bs : filteredBS) {
            pw.println(bs);
        }

        pw.close();
    }
}
