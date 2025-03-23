package kanoodle.solver.game.util;

import java.io.File;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.type.TypeReference;

import kanoodle.solver.game.Configuration;
import kanoodle.solver.game.Piece;
import kanoodle.solver.game.RawPiece;

public class ParserUtil {

    private static final String PATH_DELIMITER = "//";
    private static final String RESOURCES_PATH = String.join(PATH_DELIMITER, "src", "main", "resources");

    public static final String CONFIGS_PATH = String.join(PATH_DELIMITER, RESOURCES_PATH, "configs");
    
    public static Map<Character, Piece> parsePieces() throws Exception {
        ObjectMapper objectMapper = new ObjectMapper();
        List<RawPiece> parsedRawPieces = objectMapper.readValue(getPiecesResourceFile(), new TypeReference<List<RawPiece>>(){});

        Map<Character, Piece> pieces = new HashMap<>();
        for (RawPiece rawPiece : parsedRawPieces) pieces.put(rawPiece.letter, new Piece(rawPiece));
        return pieces;
    }

    public static Configuration parseConfiguration(int level) throws Exception {
        ObjectMapper objectMapper = new ObjectMapper();
        List<String> rows = objectMapper.readValue(getConfigResourceFile(level), new TypeReference<List<String>>(){});
        return new Configuration(level, rows);
    }

    private static File getConfigResourceFile(int level) {
        return new File(String.join(PATH_DELIMITER, CONFIGS_PATH, String.valueOf(level) + ".json"));
    }

    private static File getPiecesResourceFile() {
        return new File(String.join(PATH_DELIMITER, RESOURCES_PATH, "pieces.json"));
    }
}
